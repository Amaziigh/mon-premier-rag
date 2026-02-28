# ====================================
# PREPROCESSING — preprocessor.py
# ====================================

from llama_index.core import SimpleDirectoryReader

from config import DOCS_DIR, MIN_CONTENT_LENGTH, EXCLUDE_KEYWORDS

# ---- ÉTAPE 1 : Charger tous les documents ----
documents = SimpleDirectoryReader(DOCS_DIR).load_data()
print(f"Pages totales chargées : {len(documents)}")

# ---- ÉTAPE 2 : Filtrer par contenu minimum ----
# Si une page a moins de 100 caractères, c'est probablement
# une couverture, une page blanche, ou un titre seul
filtered = [doc for doc in documents if len(doc.text.strip()) >= MIN_CONTENT_LENGTH]
print(f"Pages après filtrage par taille : {len(filtered)}")
print(f"Pages supprimées : {len(documents) - len(filtered)}")

# ---- ÉTAPE 3 : Filtrer par mots-clés ----
# On exclut les pages qui ne contiennent que des éléments de structure
def is_structural_page(text):
    text_lower = text.lower().strip()
    # On regarde les 300 premiers caractères (le titre / en-tête de la page)
    # Si un mot-clé structurel y apparaît → c'est une page de structure
    # Avant on vérifiait la taille totale, mais une table des matières
    # avec 12 chapitres dépasse 300 chars et passait entre les mailles
    first_part = text_lower[:300]
    return any(keyword in first_part for keyword in EXCLUDE_KEYWORDS)

final = [doc for doc in filtered if not is_structural_page(doc.text)]
print(f"Pages après filtrage structurel : {len(final)}")

# ---- ÉTAPE 4 : Afficher les pages supprimées pour vérification ----
removed = [doc for doc in documents if doc not in final]
print(f"\n--- PAGES SUPPRIMÉES ({len(removed)}) ---")
for doc in removed:
    page = doc.metadata.get("page_label", "?")
    source = doc.metadata.get("file_name", "?")
    preview = doc.text.strip()[:80].replace("\n", " ")
    print(f"Page {page} ({source}) : '{preview}...'")
