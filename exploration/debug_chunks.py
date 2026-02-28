# ====================================
# VOIR LES CHUNKS — debug_chunks.py
# ====================================

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter

# ÉTAPE 1 — Charger les PDFs
documents = SimpleDirectoryReader("docs").load_data()
print(f"Nombre de documents (pages) chargés : {len(documents)}")

# ÉTAPE 2 — Découper avec les paramètres PAR DÉFAUT de LlamaIndex
parser = SentenceSplitter(chunk_size=1024, chunk_overlap=200)
chunks = parser.get_nodes_from_documents(documents)

print(f"Nombre de chunks créés : {len(chunks)}")
print(f"Taille moyenne d'un chunk : {sum(len(c.text) for c in chunks) // len(chunks)} caractères")
print()

# ÉTAPE 3 — Afficher les 3 premiers chunks pour voir à quoi ça ressemble
for i, chunk in enumerate(chunks[:3]):
    print(f"{'='*60}")
    print(f"CHUNK {i+1}")
    print(f"Taille : {len(chunk.text)} caractères")
    print(f"Source : {chunk.metadata.get('file_name', 'inconnu')}")
    print(f"Page : {chunk.metadata.get('page_label', 'inconnue')}")
    print(f"{'='*60}")
    print(chunk.text[:2000])  # On affiche les 500 premiers caractères
    print("...")
    print()