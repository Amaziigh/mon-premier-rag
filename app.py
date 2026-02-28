# ====================================
# MON PREMIER RAG — app.py
# ====================================

# ÉTAPE 0 — On importe nos outils
# Chaque ligne = un outil qu'on sort de la boîte à outils
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding

# ÉTAPE 1 — On configure la clé API
# Charge la clé depuis le fichier .env (jamais en dur dans le code !)
load_dotenv()

# ÉTAPE 2 — On choisit nos outils IA
# Le modèle d'embedding : transforme le texte en vecteurs (le bibliothécaire qui catalogue)
Settings.embed_model = GeminiEmbedding(model_name="models/gemini-embedding-001")
# Le modèle de génération : celui qui rédige les réponses (le prof qui explique)
Settings.llm = Gemini(model="models/gemini-2.5-flash")

# ÉTAPE 3 — INDEXATION (on prépare la bibliothèque)
# 3a. On lit tous les PDFs du dossier "docs"
print("Lecture des PDFs...")
documents = SimpleDirectoryReader("docs").load_data()
print(f"{len(documents)} pages chargées !")

# 3b. On découpe, on vectorise, on stocke — tout en une ligne
# C'est LlamaIndex qui fait la magie ici
print("Indexation en cours... (ça peut prendre 1-2 minutes)")
index = VectorStoreIndex.from_documents(documents)
print("Indexation terminée !")

# ÉTAPE 4 — On crée le moteur de question-réponse
query_engine = index.as_query_engine()

# ÉTAPE 5 — On pose des questions en boucle
print("\n=== TON RAG EST PRÊT ===")
print("Pose tes questions sur tes cours ! (tape quit pour sortir)\n")

while True:
    question = input("Ta question : ")
    if question.lower() == "quit":
        print("À plus !")
        break
    
    reponse = query_engine.query(question)
    print(f"\nRéponse : {reponse}\n")
