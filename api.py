# ====================================
# API FASTAPI — api.py
# ====================================
# Expose le RAG via HTTP pour le portfolio
# Usage : uvicorn api:app --reload --port 8000

import logging
import time
from collections import deque
from contextlib import asynccontextmanager

import chromadb
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini

from config import (
    CHROMA_DIR, COLLECTION_NAME,
    SIMILARITY_TOP_K, EMBEDDING_MODEL, LLM_MODEL,
    TEMPERATURE, PORTFOLIO_SYSTEM_PROMPT
)

logger = logging.getLogger("api")

# ---- ÉTAT GLOBAL ----

query_engine = None
retriever = None

# Rate limiting : 10 requêtes/minute, sliding window
RATE_LIMIT = 10
RATE_WINDOW = 60  # secondes
request_timestamps: deque = deque()


# ---- ÉTAPE 1 : Chargement de l'index au démarrage ----

@asynccontextmanager
async def lifespan(app: FastAPI):
    global query_engine, retriever

    logger.info("Chargement de l'index ChromaDB...")

    Settings.embed_model = GeminiEmbedding(model_name=EMBEDDING_MODEL)
    Settings.llm = Gemini(model=LLM_MODEL, temperature=TEMPERATURE)

    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    chroma_collection = chroma_client.get_collection(COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store)

    retriever = index.as_retriever(similarity_top_k=SIMILARITY_TOP_K)
    query_engine = index.as_query_engine(
        similarity_top_k=SIMILARITY_TOP_K,
        system_prompt=PORTFOLIO_SYSTEM_PROMPT
    )

    logger.info("Index chargé, API prête.")
    yield


# ---- ÉTAPE 2 : App FastAPI ----

app = FastAPI(
    title="RAG Portfolio API",
    description="Assistant IA d'Amazigh BELHADDAD — propulsé par RAG",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://amaziigh.github.io",
        "http://localhost:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


# ---- ÉTAPE 3 : Modèles Pydantic ----

class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)


class Source(BaseModel):
    file: str
    page: str
    score: float


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]


# ---- ÉTAPE 4 : Rate limiting ----

def check_rate_limit():
    now = time.time()
    # Retirer les timestamps hors fenêtre
    while request_timestamps and request_timestamps[0] < now - RATE_WINDOW:
        request_timestamps.popleft()
    if len(request_timestamps) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Trop de requêtes. Réessayez dans une minute.")
    request_timestamps.append(now)


# ---- ÉTAPE 5 : Endpoints ----

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    check_rate_limit()

    if query_engine is None or retriever is None:
        raise HTTPException(status_code=503, detail="Index non chargé. Réessayez plus tard.")

    try:
        results = retriever.retrieve(req.question)
        response = query_engine.query(req.question)
    except Exception as e:
        logger.error(f"Erreur lors du query: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne. Réessayez plus tard.")

    sources = []
    for r in results:
        sources.append(Source(
            file=r.node.metadata.get("file_name", "?"),
            page=r.node.metadata.get("page_label", "?"),
            score=round(r.score, 4) if r.score is not None else 0.0,
        ))

    return AskResponse(answer=str(response), sources=sources)
