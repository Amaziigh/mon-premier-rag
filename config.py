# ====================================
# CONFIGURATION — config.py
# ====================================

import os
from dotenv import load_dotenv

# Charge les variables depuis le fichier .env
# C'est plus sûr que d'écrire la clé directement dans le code
load_dotenv()

# Chemins
DOCS_DIR = "docs"
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "mes_cours"

# Paramètres de chunking
CHUNK_SIZE = 1024
CHUNK_OVERLAP = 200

# Paramètres de retrieval
SIMILARITY_TOP_K = 5

# Modèles
EMBEDDING_MODEL = "models/gemini-embedding-001"
LLM_MODEL = "models/gemini-2.5-flash"
TEMPERATURE = 0.1

# System Prompt — la personnalité de ton RAG
# C'est l'équivalent du brief qu'on donne à un consultant avant une mission :
# "voici comment tu dois te comporter avec le client"
SYSTEM_PROMPT = """Tu es un assistant pédagogique expert en Intelligence Artificielle et en RAG.

Règles :
- Tu réponds TOUJOURS en français
- Tu t'appuies UNIQUEMENT sur le contexte fourni pour répondre
- Si l'information n'est pas dans le contexte, dis-le clairement
- Tu cites la source (nom du fichier, page) quand c'est possible
- Tu structures tes réponses de manière claire et pédagogique
- Tu utilises des analogies simples pour expliquer les concepts techniques
"""

# Preprocessing — filtrage des pages inutiles
MIN_CONTENT_LENGTH = 100
EXCLUDE_KEYWORDS = ["sommaire", "table des matières", "table of contents", "remerciements"]
