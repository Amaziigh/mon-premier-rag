# ====================================
# INDEXATION — indexer.py
# ====================================

import hashlib
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.gemini import GeminiEmbedding

# On importe notre configuration centralisée
from config import (
    DOCS_DIR, CHROMA_DIR, COLLECTION_NAME,
    CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL,
    MIN_CONTENT_LENGTH, EXCLUDE_KEYWORDS
)


def get_file_hash(file_path):
    """Calcule le hash SHA256 du contenu d'un fichier."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


# ---- ÉTAPE 1 : Configurer l'embedding ----
# Pas besoin du LLM ici — l'indexation ne génère pas de réponses,
# elle ne fait que lire et vectoriser
# embed_batch_size=10 → envoie les chunks par lots de 10
# Évite le timeout (DeadlineExceeded) avec beaucoup de documents
Settings.embed_model = GeminiEmbedding(model_name=EMBEDDING_MODEL, embed_batch_size=10)
Settings.node_parser = SentenceSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)

# ---- ÉTAPE 2 : Préparer ChromaDB ----
# PersistentClient = les données survivent à l'arrêt du programme
# C'est la différence avec ce qu'on faisait avant (tout en RAM)
print(f"Initialisation de ChromaDB dans '{CHROMA_DIR}'...")
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)

# Une "collection" dans ChromaDB, c'est comme une table dans BigQuery
# ou un Drive partagé — un espace dédié à un ensemble de données
chroma_collection = chroma_client.get_or_create_collection(COLLECTION_NAME)
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Récupérer les hashes des fichiers déjà indexés
existing = chroma_collection.get(include=["metadatas"])
existing_hashes = {
    meta.get("file_hash")
    for meta in existing["metadatas"]
    if meta.get("file_hash")
}
print(f"{len(existing_hashes)} fichier(s) déjà indexé(s) détecté(s)")

# ---- ÉTAPE 3 : Charger et filtrer les documents ----
print(f"Lecture des PDFs dans '{DOCS_DIR}'...")
documents = SimpleDirectoryReader(DOCS_DIR).load_data()
print(f"{len(documents)} pages chargées")

# Filtrage : on retire les pages trop courtes (couvertures, pages blanches)
# et les pages structurelles (sommaire, table des matières)
def is_structural_page(text):
    first_part = text.lower().strip()[:300]
    return any(keyword in first_part for keyword in EXCLUDE_KEYWORDS)

documents = [doc for doc in documents if len(doc.text.strip()) >= MIN_CONTENT_LENGTH]
documents = [doc for doc in documents if not is_structural_page(doc.text)]
print(f"{len(documents)} pages retenues après filtrage")

# Filtrage par hash : ne garder que les documents de fichiers non encore indexés
new_documents = []
seen_hashes = set()
for doc in documents:
    file_path = doc.metadata.get("file_path", "")
    if not file_path:
        continue
    file_hash = get_file_hash(file_path)
    if file_hash not in existing_hashes and file_hash not in seen_hashes:
        doc.metadata["file_hash"] = file_hash
        new_documents.append(doc)
        seen_hashes.add(file_hash)
    elif file_hash not in existing_hashes:
        # Même fichier (hash déjà vu dans cette exécution), autre page
        doc.metadata["file_hash"] = file_hash
        new_documents.append(doc)

skipped = len(documents) - len(new_documents)
if skipped > 0:
    print(f"{skipped} page(s) ignorée(s) (fichiers déjà indexés)")

# ---- ÉTAPE 4 : Indexer ----
if not new_documents:
    print("\nTous les documents sont déjà indexés — rien à faire.")
else:
    print(f"\n{len(new_documents)} nouvelle(s) page(s) à indexer...")
    print("Indexation en cours...")
    index = VectorStoreIndex.from_documents(
        new_documents,
        storage_context=storage_context
    )
    print("Indexation terminée !")

# ---- ÉTAPE 5 : Vérification ----
count = chroma_collection.count()
print(f"\nChunks stockés dans ChromaDB : {count}")
print(f"Données persistées dans le dossier '{CHROMA_DIR}'")
print(f"\nTu peux maintenant lancer 'python query.py' pour poser des questions.")
