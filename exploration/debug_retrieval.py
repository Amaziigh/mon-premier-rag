# ====================================
# VOIR LE RETRIEVAL — debug_retrieval.py
# ====================================

import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding

os.environ["GOOGLE_API_KEY"] = "REMOVED_API_KEY"

Settings.embed_model = GeminiEmbedding(model_name="models/gemini-embedding-001")
Settings.llm = Gemini(model="models/gemini-2.5-flash")

# Charger et indexer
documents = SimpleDirectoryReader("docs").load_data()
index = VectorStoreIndex.from_documents(documents)

# IMPORTANT : on crée un RETRIEVER, pas un query_engine
# Le retriever cherche les morceaux pertinents SANS générer de réponse
retriever = index.as_retriever(similarity_top_k=5)
# similarity_top_k=5 → ramène les 5 morceaux les plus pertinents

print("=== MODE DEBUG RETRIEVAL ===")
print("Pose une question pour voir quels chunks sont récupérés\n")

while True:
    question = input("Ta question : ")
    if question.lower() == "quit":
        break
    
    # Récupérer les chunks pertinents
    results = retriever.retrieve(question)
    
    print(f"\n{'='*60}")
    print(f"QUESTION : {question}")
    print(f"CHUNKS RÉCUPÉRÉS : {len(results)}")
    print(f"{'='*60}\n")
    
    for i, result in enumerate(results):
        score = result.score  # Score de similarité (0 à 1)
        text = result.node.text
        source = result.node.metadata.get("file_name", "inconnu")
        page = result.node.metadata.get("page_label", "?")
        
        print(f"--- Chunk {i+1} | Score: {score:.4f} | Source: {source} | Page: {page} ---")
        print(text[:300])  # 300 premiers caractères
        print("...\n")