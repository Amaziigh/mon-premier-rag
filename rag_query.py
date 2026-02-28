# ====================================
# QUERY CLI — rag_query.py
# ====================================
# Version non-interactive de query.py
# Usage : python rag_query.py "ta question ici"

import sys
import chromadb
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini

from config import (
    CHROMA_DIR, COLLECTION_NAME,
    SIMILARITY_TOP_K, EMBEDDING_MODEL, LLM_MODEL,
    TEMPERATURE, SYSTEM_PROMPT
)

# ---- ÉTAPE 1 : Vérifier l'argument ----
if len(sys.argv) < 2:
    print("Usage : python rag_query.py \"ta question ici\"")
    sys.exit(1)

question = sys.argv[1]

# ---- ÉTAPE 2 : Configurer les modèles ----
Settings.embed_model = GeminiEmbedding(model_name=EMBEDDING_MODEL)
Settings.llm = Gemini(model=LLM_MODEL, temperature=TEMPERATURE)

# ---- ÉTAPE 3 : Charger l'index depuis ChromaDB ----
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
chroma_collection = chroma_client.get_collection(COLLECTION_NAME)
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
index = VectorStoreIndex.from_vector_store(vector_store)

# ---- ÉTAPE 4 : Récupérer les chunks + générer la réponse ----
retriever = index.as_retriever(similarity_top_k=SIMILARITY_TOP_K)
results = retriever.retrieve(question)

query_engine = index.as_query_engine(
    similarity_top_k=SIMILARITY_TOP_K,
    system_prompt=SYSTEM_PROMPT
)
response = query_engine.query(question)

# ---- ÉTAPE 5 : Afficher résultat ----
print(f"\nRÉPONSE :\n{response}\n")

print("SOURCES :")
for i, r in enumerate(results):
    fichier = r.node.metadata.get("file_name", "?")
    page = r.node.metadata.get("page_label", "?")
    score = r.score if r.score is not None else 0.0
    print(f"{i+1}. {fichier} (p.{page}) — Score: {score:.2f}")
