# Mon Premier RAG

Système RAG (Retrieval Augmented Generation) éducatif qui transforme des PDFs en base de connaissances interrogeable par IA.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![LlamaIndex](https://img.shields.io/badge/LlamaIndex-0.14-purple)
![Gemini](https://img.shields.io/badge/Gemini-2.5--flash-orange)
![ChromaDB](https://img.shields.io/badge/ChromaDB-1.5-green)

---

## Ce que c'est

Un projet d'apprentissage du RAG construit brique par brique, avec un triple objectif :

1. **Monter en compétence** — comprendre chaque composant du pipeline RAG
2. **Créer un portfolio** — un cas d'usage concret publiable sur GitHub
3. **Préparer une formation** — documenter le parcours pour en faire du contenu pédagogique

Le cas d'usage cible : proposer un système RAG aux clients après une migration de données vers Google Drive — transformer des documents migrés en base de connaissances interrogeable par IA.

---

## Architecture

```
                        INDEXATION (une seule fois)
PDFs ──→ Preprocessing ──→ Chunking ──→ Embeddings ──→ ChromaDB
                                                          │
                        INTERROGATION (à chaque question) │
Question ──→ Embedding ──→ Recherche sémantique ──────────┘
                                    │
                              Top K chunks ──→ LLM ──→ Réponse + Sources
```

---

## Stack technique

| Composant | Technologie | Rôle |
|-----------|-------------|------|
| Framework RAG | LlamaIndex 0.14 | Orchestration du pipeline |
| LLM | Gemini 2.5-flash | Génération des réponses |
| Embeddings | Gemini Embedding 001 | Vectorisation du texte |
| Base vectorielle | ChromaDB | Stockage persistant des vecteurs |
| Interface web | Streamlit | Chat interactif dans le navigateur |
| Extraction PDF | pypdf + PyMuPDF | Lecture texte et images |
| Vision | Gemini Vision | Description d'images (RAG multimodal) |

---

## Démarrage rapide

### Prérequis

- Python 3.11+
- Une clé API Google (Gemini)

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/I-Tayri/mon-premier-rag.git
cd mon-premier-rag

# Créer et activer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install llama-index llama-index-embeddings-gemini llama-index-llms-gemini \
            llama-index-vector-stores-chroma chromadb \
            pypdf pymupdf streamlit python-dotenv google-generativeai pillow
```

### Configuration

```bash
# Créer le fichier .env avec ta clé API
echo "GOOGLE_API_KEY=ta_clé_ici" > .env
```

### Utilisation

```bash
# 1. Placer des PDFs dans le dossier docs/
mkdir -p docs
# (copier tes PDFs dans docs/)

# 2. Indexer les documents (une seule fois)
python indexer.py

# 3. Interroger — au choix :
python query.py                          # Mode interactif (boucle de questions)
python rag_query.py "ta question ici"    # Mode CLI (une question, une réponse)
python -m streamlit run ui.py            # Interface web (http://localhost:8501)
```

---

## Structure du projet

```
mon-premier-rag/
├── config.py             # Configuration centralisée (modèles, paramètres)
├── indexer.py            # Indexation des PDFs dans ChromaDB
├── query.py              # Interface interactive (boucle CLI)
├── rag_query.py          # CLI non-interactif (question → réponse)
├── ui.py                 # Interface web Streamlit
├── preprocessor.py       # Filtrage des pages inutiles
├── extract_images.py     # Extraction d'images + descriptions (multimodal)
├── app.py                # Premier prototype (RAG en mémoire)
├── exploration/          # Scripts de debug et d'exploration
│   ├── debug_chunks.py       # Visualiser les chunks créés
│   ├── debug_overlap.py      # Visualiser le chevauchement
│   ├── debug_params.py       # Tester différentes configurations
│   ├── debug_retrieval.py    # Scores de similarité détaillés
│   ├── demo_overlap.py       # Démo chunking sur texte synthétique
│   └── test_api.py           # Vérifier les modèles disponibles
├── docs/                 # PDFs à indexer (gitignored)
├── chroma_db/            # Base vectorielle persistante (gitignored)
├── FORMATION.md          # Notes pédagogiques (8 modules)
├── ROADMAP.md            # Feuille de route du projet
└── .env                  # Clé API (gitignored)
```

---

## Parcours d'apprentissage

Ce projet a été construit brique par brique, en suivant une approche progressive documentée dans [`FORMATION.md`](FORMATION.md) :

| Module | Thème |
|--------|-------|
| 0 | Le schéma mental — comprendre le RAG avec l'analogie de la bibliothèque |
| 1 | Setup — environnement Python, LlamaIndex, Gemini |
| 2 | Premier RAG — `app.py`, pipeline en mémoire |
| 3 | Sous le capot — chunking, embeddings, retrieval, paramètres |
| 4 | Persistance — ChromaDB, séparation indexation/interrogation |
| 5 | Personnalisation — system prompt, temperature, preprocessing |
| 6 | Interface web — Streamlit, cache, historique de conversation |
| 7 | RAG multimodal — extraction d'images, Gemini Vision |

La feuille de route complète est dans [`ROADMAP.md`](ROADMAP.md).

---

## Auteur

**Amazigh BELHADDAD** — Consultant Google Workspace & Développeur en formation

- GitHub : [I-Tayri](https://github.com/I-Tayri)
- LinkedIn : [amazighbelhaddad](https://www.linkedin.com/in/amazighbelhaddad)
