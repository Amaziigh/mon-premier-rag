# ====================================
# VOIR LE CHEVAUCHEMENT — debug_overlap.py
# ====================================

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter

# Charger les PDFs
documents = SimpleDirectoryReader("docs").load_data()

# Découper avec overlap
parser = SentenceSplitter(chunk_size=1024, chunk_overlap=200)
chunks = parser.get_nodes_from_documents(documents)

print(f"Nombre total de chunks : {len(chunks)}\n")

# Trouver des chunks consécutifs de la même page (= là où il y a eu découpe)
for i in range(len(chunks) - 1):
    chunk_actuel = chunks[i]
    chunk_suivant = chunks[i + 1]

    # Vérifier si les deux chunks viennent du même fichier et de la même page
    meme_fichier = chunk_actuel.metadata.get('file_name') == chunk_suivant.metadata.get('file_name')
    meme_page = chunk_actuel.metadata.get('page_label') == chunk_suivant.metadata.get('page_label')

    if meme_fichier and meme_page:
        print("=" * 70)
        print(f"CHEVAUCHEMENT TROUVÉ !")
        print(f"Fichier : {chunk_actuel.metadata.get('file_name')}")
        print(f"Page : {chunk_actuel.metadata.get('page_label')}")
        print("=" * 70)

        # Fin du chunk actuel (200 derniers caractères)
        fin_chunk_actuel = chunk_actuel.text[-250:]

        # Début du chunk suivant (200 premiers caractères)
        debut_chunk_suivant = chunk_suivant.text[:250]

        print(f"\n🔵 FIN DU CHUNK {i+1} (250 derniers caractères):")
        print("-" * 50)
        print(fin_chunk_actuel)
        print("-" * 50)

        print(f"\n🟢 DÉBUT DU CHUNK {i+2} (250 premiers caractères):")
        print("-" * 50)
        print(debut_chunk_suivant)
        print("-" * 50)

        # Trouver le texte en commun
        for longueur in range(min(200, len(fin_chunk_actuel), len(debut_chunk_suivant)), 10, -1):
            if fin_chunk_actuel[-longueur:] == debut_chunk_suivant[:longueur]:
                print(f"\n🔴 ZONE DE CHEVAUCHEMENT ({longueur} caractères en commun):")
                print("-" * 50)
                print(fin_chunk_actuel[-longueur:])
                print("-" * 50)
                break

        print("\n")
        break  # On montre juste le premier exemple

else:
    print("Aucun chevauchement trouvé sur la même page.")
    print("Cela signifie que chaque page fait moins de 1024 caractères.")
    print("\nMontrons quand même la fin d'un chunk et le début du suivant :")
    print("=" * 70)

    # Montrer chunks 1 et 2 même s'ils sont de pages différentes
    print(f"\n🔵 FIN DU CHUNK 1 (150 derniers caractères):")
    print(f"   Page : {chunks[0].metadata.get('page_label')}")
    print("-" * 50)
    print(chunks[0].text[-150:])

    print(f"\n🟢 DÉBUT DU CHUNK 2 (150 premiers caractères):")
    print(f"   Page : {chunks[1].metadata.get('page_label')}")
    print("-" * 50)
    print(chunks[1].text[:150])

    print("\n⚠️  Pas de chevauchement ici car ce sont des pages différentes.")
