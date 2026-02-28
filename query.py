# ====================================
# INTERROGATION — query.py
# ====================================

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

# ---- ÉTAPE 1 : Configurer les modèles ----
Settings.embed_model = GeminiEmbedding(model_name=EMBEDDING_MODEL)
# temperature=0.1 → réponses stables et fidèles au contenu
# Avant c'était le défaut (~0.7) → réponses qui variaient à chaque fois
Settings.llm = Gemini(model=LLM_MODEL, temperature=TEMPERATURE)

# ---- ÉTAPE 2 : Charger l'index EXISTANT depuis ChromaDB ----
# C'est ici que tout change : on ne relit PAS les PDFs
# On charge directement les vecteurs déjà calculés
print("Chargement de l'index depuis ChromaDB...")
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
chroma_collection = chroma_client.get_collection(COLLECTION_NAME)
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# VectorStoreIndex.from_vector_store → charge depuis le stockage existant
# Avant on utilisait from_documents → créait tout depuis zéro
index = VectorStoreIndex.from_vector_store(vector_store)

print(f"Index chargé ! ({chroma_collection.count()} chunks disponibles)")

# ---- ÉTAPE 3 : Mode question-réponse ----
# system_prompt → les instructions invisibles qui cadrent le comportement du LLM
# C'est grâce à ça que le RAG répond en français et cite ses sources
query_engine = index.as_query_engine(
    similarity_top_k=SIMILARITY_TOP_K,
    system_prompt=SYSTEM_PROMPT
)

print("\n=== RAG PERSISTANT PRÊT ===")
print("Tes vecteurs sont chargés depuis le disque, pas recalculés !")
print("Tape 'quit' pour sortir, 'debug' pour voir les chunks récupérés\n")

while True:
    question = input("Ta question : ")

    if question.lower() == "quit":
        print("À plus !")
        break

    # Mode debug : afficher les chunks récupérés + la réponse
    if question.lower() == "debug":
        question = input("Question (mode debug) : ")
        retriever = index.as_retriever(similarity_top_k=SIMILARITY_TOP_K)
        results = retriever.retrieve(question)

        print(f"\n--- CHUNKS RÉCUPÉRÉS ---")
        for i, r in enumerate(results):
            print(f"Chunk {i+1} | Score: {r.score:.4f} | "
                  f"Source: {r.node.metadata.get('file_name', '?')} | "
                  f"Page: {r.node.metadata.get('page_label', '?')}")
            print(f"Extrait: {r.node.text[:200]}...\n")

        response = query_engine.query(question)
        print(f"--- RÉPONSE ---\n{response}\n")
    else:
        response = query_engine.query(question)
        print(f"\nRéponse : {response}\n")
