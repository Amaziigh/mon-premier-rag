# ====================================
# DÉMONSTRATION DU CHEVAUCHEMENT
# ====================================

# Simulons un texte long pour voir le découpage
texte_long = """
La vectorisation est un concept fondamental en intelligence artificielle.
Elle permet de transformer du texte en nombres que les machines peuvent comprendre.
Chaque mot ou phrase devient un point dans un espace à plusieurs dimensions.
Les concepts similaires se retrouvent proches les uns des autres dans cet espace.
Par exemple, "roi" et "reine" seront plus proches que "roi" et "voiture".
C'est grâce à cette propriété que la recherche sémantique fonctionne.
Le RAG utilise cette technique pour trouver les passages pertinents.
Quand tu poses une question, elle est vectorisée puis comparée aux chunks.
Les chunks les plus proches sont récupérés et envoyés au LLM.
Le LLM génère alors une réponse basée sur ces informations contextuelles.
C'est ce qui permet d'avoir des réponses précises basées sur tes documents.
Sans la vectorisation, on serait limité à la recherche par mots-clés exacts.
La recherche sémantique comprend le sens, pas juste les mots.
""".strip()

print(f"Texte original : {len(texte_long)} caractères\n")
print("=" * 70)
print("TEXTE COMPLET :")
print("=" * 70)
print(texte_long)
print()

# Paramètres de découpage
chunk_size = 300  # Plus petit pour la démo
overlap = 100     # Chevauchement de 100 caractères

print("=" * 70)
print(f"DÉCOUPAGE : chunk_size={chunk_size}, overlap={overlap}")
print("=" * 70)

# Découpage manuel pour montrer le concept
chunks = []
debut = 0
numero = 1

while debut < len(texte_long):
    fin = min(debut + chunk_size, len(texte_long))
    chunk = texte_long[debut:fin]
    chunks.append(chunk)

    print(f"\n📦 CHUNK {numero}")
    print(f"   Position : caractères {debut} à {fin}")
    print(f"   Taille : {len(chunk)} caractères")
    print("-" * 50)
    print(chunk)
    print("-" * 50)

    # Prochain chunk commence overlap caractères AVANT la fin
    debut = fin - overlap
    numero += 1

    if fin >= len(texte_long):
        break

# Montrer le chevauchement entre chunk 1 et 2
print("\n" + "=" * 70)
print("🔴 ZONE DE CHEVAUCHEMENT (chunks 1 et 2)")
print("=" * 70)

fin_chunk1 = chunks[0][-overlap:]
debut_chunk2 = chunks[1][:overlap]

print(f"\nFin du chunk 1 ({overlap} derniers caractères):")
print(f'"{fin_chunk1}"')

print(f"\nDébut du chunk 2 ({overlap} premiers caractères):")
print(f'"{debut_chunk2}"')

if fin_chunk1 == debut_chunk2:
    print("\n✅ IDENTIQUES ! C'est le chevauchement.")
else:
    print("\n⚠️  Légère différence (due aux coupures de mots)")
