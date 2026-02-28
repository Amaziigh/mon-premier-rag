# ROADMAP — Mon Premier RAG

## Vision

Partir d'un prototype RAG éducatif pour arriver à un projet portfolio professionnel, tout en documentant le parcours pour en faire une formation.

Cas d'usage cible : proposer un système RAG aux clients après une migration de données vers Google Drive — transformer des documents migrés en base de connaissances interrogeable par IA.

---

## Phase 1 — Comprendre les fondations ⬅️ EN COURS

Objectif : maîtriser chaque brique du pipeline RAG individuellement.

- [ ] Comprendre les embeddings (ce que c'est, comment ça marche)
- [ ] Comprendre le chunking (découpage, taille, chevauchement)
- [ ] Comprendre le retrieval (recherche sémantique, scores de similarité)
- [ ] Comprendre la génération (prompt augmenté, rôle du LLM)
- [ ] Comprendre le pipeline complet (comment les briques s'assemblent)

Livrables : scripts `debug_*.py` et `demo_*.py` fonctionnels avec commentaires.

---

## Phase 2 — Solidifier le projet

Objectif : passer du prototype au projet structuré.

- [ ] Gérer la clé API proprement (`.env` + `python-dotenv`)
- [ ] Créer un `requirements.txt`
- [ ] Structurer le code (séparer configuration, indexation, query)
- [ ] Ajouter une interface web (Streamlit ou Gradio)
- [ ] Tester avec différents types de documents
- [ ] Initialiser le dépôt Git

---

## Phase 3 — Projet portfolio

Objectif : un projet concret, démontrable, lié à l'expertise Google Workspace.

- [ ] Définir le cas d'usage final (ex : assistant post-migration Google Drive)
- [ ] Implémenter les fonctionnalités avancées (multi-documents, filtrage, historique)
- [ ] Soigner le README GitHub (démo, screenshots, explication claire)
- [ ] Déployer une version en ligne (Streamlit Cloud, HuggingFace Spaces, ou autre)

---

## Phase 4 — Contenu formation

Objectif : transformer le parcours d'apprentissage en formation structurée.

- [ ] Documenter chaque concept appris avec des exemples pratiques
- [ ] Structurer en modules progressifs
- [ ] Préparer les supports pour le site web

---

## Suivi de progression

| Date | Ce qu'on a fait |
|------|----------------|
| 2026-02-25 | Setup initial : `app.py` fonctionnel, scripts de debug, pipeline RAG basique avec LlamaIndex + Gemini |
| 2026-02-28 | Ajout `rag_query.py` — accès CLI non-interactif au RAG (question → réponse + sources en une commande) |
