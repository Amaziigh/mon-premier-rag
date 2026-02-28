# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Contexte utilisateur

Développeur freelance, Consultant Google Workspace. Expertise : Google Sheets, Apps Script, AppSheet, migration de données, automatisation de processus. Formation autodidacte. En apprentissage de l'IA et du RAG pour élargir son offre de services.

## Projet

Projet d'apprentissage RAG avec un triple objectif :

1. **Monter en compétence** — comprendre le RAG brique par brique en suivant un cours (claude.ai)
2. **Créer un projet portfolio** — un cas d'usage concret et innovant à publier sur GitHub
3. **Préparer du contenu formation** — documenter l'apprentissage pour créer une formation sur son site web

Le projet est un système RAG éducatif en Python qui indexe des PDFs (texte + images) depuis `docs/` et répond aux questions via CLI, interface web Streamlit, ou commande directe.

## Approche pédagogique

- On avance brique par brique, sans brûler les étapes
- L'utilisateur partage les instructions de son cours, on les met en pratique ensemble
- Expliquer le "pourquoi" derrière chaque concept, pas juste le "comment"
- L'utilisateur code, Claude accompagne — ne pas tout faire à sa place
- **Ne jamais installer, ajouter ou changer un outil/framework/plugin sans validation explicite** — proposer, expliquer les options, décider ensemble
- Voir `ROADMAP.md` pour le plan détaillé et le suivi de progression

## Stack technique

- **Python 3.11** avec environnement virtuel local (`venv/`)
- **LlamaIndex 0.14** — framework RAG (indexation, chunking, query engine)
- **Google Gemini** — LLM (`gemini-2.5-flash`) et embeddings (`gemini-embedding-001`)
- **ChromaDB** — base vectorielle persistante (`chroma_db/`)
- **PyMuPDF (fitz)** — extraction d'images des PDFs
- **pypdf** — lecture du texte des PDFs
- **Streamlit** — interface web

## Commandes

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Lancer l'application RAG interactive
python app.py

# Indexer les documents (détecte les doublons via hash SHA256)
python indexer.py

# Extraire et décrire les images des PDFs (Gemini Vision)
python extract_images.py

# Interroger le RAG
python query.py              # Mode interactif (boucle CLI)
python rag_query.py "question"  # Mode non-interactif (une commande)
streamlit run ui.py          # Interface web

# Scripts de débogage
python debug_chunks.py       # Visualiser les chunks créés
python debug_overlap.py      # Visualiser le chevauchement entre chunks
python debug_params.py       # Tester différentes configurations de chunking
python debug_retrieval.py    # Mode debug avec scores de similarité
python demo_overlap.py       # Démo du chunking sur texte synthétique
python test_api.py           # Vérifier les modèles Google disponibles
python preprocessor.py       # Tester le filtrage des pages
```

## Architecture

```
docs/              → PDFs sources + descriptions d'images (.txt)
extracted_images/  → Images extraites des PDFs
chroma_db/         → Base vectorielle persistante
config.py          → Configuration centralisée (chemins, modèles, paramètres)
indexer.py         → Indexation avec détection de doublons (hash SHA256)
extract_images.py  → Extraction d'images + description via Gemini Vision
query.py           → Interface CLI interactive
rag_query.py       → Query en une commande (non-interactif)
ui.py              → Interface web Streamlit
app.py             → Script original (pipeline complet)
preprocessor.py    → Test du filtrage des pages
debug_*.py         → Scripts d'exploration autonomes
```

Pipeline : `extract_images.py` (images → descriptions .txt) → `indexer.py` (PDFs + .txt → chunks → embeddings → ChromaDB) → `query.py` / `rag_query.py` / `ui.py` (question → retrieval → réponse)

## Conventions de code

- HTML sémantique (header, main, section, footer)
- CSS : méthodologie BEM pour le nommage des classes
- JavaScript : vanilla uniquement, pas de framework ni librairie
- Variables et fonctions en anglais
- Contenu visible en français
- Mobile-first : concevoir d'abord pour mobile, puis adapter pour desktop
- Structure par sections numérotées (ÉTAPE 1, 2, 3…) dans les scripts
