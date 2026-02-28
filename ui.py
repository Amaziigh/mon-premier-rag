# ====================================
# INTERFACE WEB — ui.py
# ====================================

import streamlit as st
import chromadb
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini

from config import (
    CHROMA_DIR, COLLECTION_NAME, SIMILARITY_TOP_K,
    EMBEDDING_MODEL, LLM_MODEL, TEMPERATURE, SYSTEM_PROMPT
)

# ---- Configuration de la page ----
st.set_page_config(
    page_title="Mon RAG - Assistant IA",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Assistant IA — Cours & Documentation")
st.caption("Pose des questions sur tes cours. Le RAG cherche dans tes documents et te répond.")

# ---- Chargement de l'index (une seule fois grâce au cache Streamlit) ----
@st.cache_resource
def load_index():
    """Charge l'index ChromaDB une seule fois, même si la page se rafraîchit."""
    Settings.embed_model = GeminiEmbedding(model_name=EMBEDDING_MODEL)
    Settings.llm = Gemini(model=LLM_MODEL, temperature=TEMPERATURE)

    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    chroma_collection = chroma_client.get_collection(COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store)

    return index, chroma_collection.count()

index, chunk_count = load_index()

# ---- Sidebar : infos et paramètres ----
with st.sidebar:
    st.header("📊 Infos du système")
    st.metric("Chunks indexés", chunk_count)
    st.metric("Modèle LLM", LLM_MODEL.split("/")[-1])
    st.metric("Temperature", TEMPERATURE)

    st.divider()

    # Permettre à l'utilisateur de régler le nombre de sources
    top_k = st.slider(
        "Nombre de sources à consulter",
        min_value=1,
        max_value=10,
        value=SIMILARITY_TOP_K,
        help="Plus c'est élevé, plus le RAG consulte de passages. "
             "Trop élevé = risque de bruit."
    )

    show_sources = st.checkbox("Afficher les sources", value=True)

    st.divider()
    st.caption("RAG construit avec LlamaIndex + ChromaDB + Gemini")

# ---- Historique de conversation ----
# st.session_state persiste entre les interactions de l'utilisateur
# C'est la "mémoire" de la session web
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---- Zone de saisie ----
question = st.chat_input("Pose ta question ici...")

if question:
    # Afficher la question de l'utilisateur
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})

    # Générer la réponse
    with st.chat_message("assistant"):
        with st.spinner("Recherche dans les documents..."):
            # Récupérer les chunks pertinents
            retriever = index.as_retriever(similarity_top_k=top_k)
            results = retriever.retrieve(question)

            # Générer la réponse
            query_engine = index.as_query_engine(
                similarity_top_k=top_k,
                system_prompt=SYSTEM_PROMPT
            )
            response = query_engine.query(question)

            # Afficher la réponse
            st.markdown(str(response))

            # Afficher les sources si demandé
            if show_sources and results:
                st.divider()
                st.caption("📚 Sources consultées :")
                for i, r in enumerate(results):
                    source = r.node.metadata.get("file_name", "inconnu")
                    page = r.node.metadata.get("page_label", "?")
                    score = r.score

                    with st.expander(
                        f"Source {i+1} — {source} (p.{page}) — "
                        f"Score: {score:.2f}"
                    ):
                        st.markdown(r.node.text[:500] + "...")

    # Sauvegarder la réponse dans l'historique
    st.session_state.messages.append({
        "role": "assistant",
        "content": str(response)
    })
