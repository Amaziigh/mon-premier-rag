# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Contexte utilisateur

Développeur freelance, Consultant Google Workspace. Expertise : Google Sheets, Apps Script, AppSheet, migration de données, automatisation de processus. Formation autodidacte. En apprentissage de l'IA et du RAG pour élargir son offre de services.

## Projet

Projet d'apprentissage RAG avec un triple objectif :

1. **Monter en compétence** — comprendre le RAG brique par brique en suivant un cours (claude.ai)
2. **Créer un projet portfolio** — un cas d'usage concret et innovant à publier sur GitHub
3. **Préparer du contenu formation** — documenter l'apprentissage pour créer une formation sur son site web

Le projet est actuellement un système RAG éducatif en Python qui indexe des PDFs depuis `docs/` et répond aux questions via une interface CLI.

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
- **pypdf** — lecture des fichiers PDF

## Commandes

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Lancer l'application RAG interactive
python app.py

# Scripts de débogage
python debug_chunks.py       # Visualiser les chunks créés
python debug_overlap.py      # Visualiser le chevauchement entre chunks
python debug_params.py       # Tester différentes configurations de chunking
python debug_retrieval.py    # Mode debug avec scores de similarité
python demo_overlap.py       # Démo du chunking sur texte synthétique
python test_api.py           # Vérifier les modèles Google disponibles

# Interroger le RAG en une commande (non-interactif)
python rag_query.py "ta question ici"
```

Pas de `requirements.txt` — les dépendances sont installées dans `venv/`.

## Architecture

> Architecture évolutive — sera restructurée au fur et à mesure de l'apprentissage (voir ROADMAP.md Phase 2).

État actuel : script unique `app.py` avec pipeline RAG linéaire (chargement PDFs → chunking → indexation → query engine → boucle CLI). Les fichiers `debug_*.py` et `demo_*.py` sont des scripts d'exploration autonomes.

## Conventions de code

- HTML sémantique (header, main, section, footer)
- CSS : méthodologie BEM pour le nommage des classes
- JavaScript : vanilla uniquement, pas de framework ni librairie
- Variables et fonctions en anglais
- Contenu visible en français
- Mobile-first : concevoir d'abord pour mobile, puis adapter pour desktop
- Structure par sections numérotées (ÉTAPE 1, 2, 3…) dans les scripts
-
