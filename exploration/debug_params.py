# ====================================
# TESTER LES PARAMÈTRES — debug_params.py
# ====================================

import os
import time
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding

os.environ["GOOGLE_API_KEY"] = ""

# embed_batch_size=10 → envoie les chunks par lots de 10 au lieu de tout d'un coup
# Ça évite le timeout (DeadlineExceeded) avec beaucoup de petits chunks
Settings.embed_model = GeminiEmbedding(model_name="models/gemini-embedding-001", embed_batch_size=10)
Settings.llm = Gemini(model="models/gemini-2.5-flash")

documents = SimpleDirectoryReader("docs").load_data()

# ====================================
# EXPÉRIENCE 1 : Impact de la taille des chunks
# ====================================

question = "quels sont les niveaux de maturité d'un RAG ?"

configs = [
    {"name": "Gros chunks",    "chunk_size": 2048, "chunk_overlap": 400},
    {"name": "Chunks moyens",  "chunk_size": 1024, "chunk_overlap": 200},
    {"name": "Petits chunks",  "chunk_size": 256,  "chunk_overlap": 50}
]

for config in configs:
    print(f"\n{'='*60}")
    print(f"CONFIG : {config['name']} (size={config['chunk_size']}, overlap={config['chunk_overlap']})")
    print(f"{'='*60}")
    
    # Redécouper avec ces paramètres
    parser = SentenceSplitter(
        chunk_size=config["chunk_size"],
        chunk_overlap=config["chunk_overlap"]
    )
    
    Settings.node_parser = parser

    # Compter les chunks AVANT l'indexation (pas d'appel API)
    chunks = parser.get_nodes_from_documents(documents)
    print(f"Nombre total de chunks : {len(chunks)}")
    print("Indexation en cours...")

    index = VectorStoreIndex.from_documents(documents)

    retriever = index.as_retriever(similarity_top_k=3)
    results = retriever.retrieve(question)
    print(f"Scores : {[f'{r.score:.4f}' for r in results]}")
    
    # Générer la réponse
    query_engine = index.as_query_engine(similarity_top_k=3)
    response = query_engine.query(question)
    print(f"\nRéponse : {str(response)[:400]}...")