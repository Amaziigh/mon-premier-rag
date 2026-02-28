# FORMATION RAG — Notes de parcours

> Matière brute pour créer une formation web. Chaque module correspond à une étape d'apprentissage.
> Les FAQ capturent les vraies questions d'un débutant — c'est ça qui fait une bonne formation.

---

## Module 0 — Le schéma mental

### Concepts clés
- **RAG** = Retrieval Augmented Generation. Le nom décrit le process : on Récupère, on Augmente, on Génère.
- Analogie de la bibliothèque : tu as 200 livres, un visiteur pose une question. Tu ne relis pas tout — tu cherches les 3-4 pages pertinentes, tu les relis, et tu réponds avec tes mots.
- Trois acteurs, trois étapes, toujours dans cet ordre :
  - **Indexation** (une seule fois) — on prépare la bibliothèque. Découper, vectoriser, stocker.
  - **Retrieval** (à chaque question) — le bibliothécaire cherche les morceaux pertinents.
  - **Generation** (à chaque question) — le LLM répond en s'appuyant sur les morceaux trouvés.

### Le pipeline complet en entreprise
- Migration → Structuration/Nettoyage → RAG → Interface/Agents
- Migrer des données vers le cloud ne suffit pas — il faut les rendre exploitables par l'IA.

### FAQ Apprenant

> Pourquoi le RAG plutôt que donner tous les documents directement à l'IA ?
→ Les LLM ont une limite de contexte (nombre de tokens qu'ils peuvent lire en une fois). On ne peut pas envoyer 200 PDFs d'un coup. Le RAG sélectionne uniquement les passages pertinents.

> C'est quoi la différence entre RAG et fine-tuning ?
→ Le fine-tuning modifie le modèle lui-même (cher, complexe, figé). Le RAG connecte le modèle à des données externes sans le modifier — plus flexible, moins cher, les données peuvent changer.

---

## Module 1 — Préparer l'atelier

### Concepts clés
- **Environnement virtuel (venv)** — une bulle isolée pour le projet. Les bibliothèques installées dedans n'affectent pas le reste de la machine. Comme un Drive partagé dédié à un projet.
- **pip** — le gestionnaire de paquets Python. L'équivalent du Play Store pour des bibliothèques de code.

### Les outils et leur rôle

| Paquet | Rôle | Analogie |
|--------|------|----------|
| `llama-index` | Chef d'orchestre du RAG | Le consultant qui coordonne la migration |
| `llama-index-llms-gemini` | Connecteur vers Gemini (génération) | Le connecteur vers l'environnement cible |
| `llama-index-embeddings-gemini` | Transforme le texte en vecteurs | Le catalogage des fichiers |
| `pypdf` | Lit les fichiers PDF | L'outil de lecture des fichiers source |

### FAQ Apprenant

> C'est quoi LlamaIndex ? C'est lié à LLaMA de Meta ?
→ Non, aucun lien. LLaMA (Meta) est un modèle d'IA (un cerveau). LlamaIndex est un framework (de la plomberie) qui connecte tes données à n'importe quel modèle d'IA. Le nom est juste du marketing.

> Quels sont les équivalents de LlamaIndex ?
→ **LangChain** (plus généraliste, plus complexe), **Haystack** (orienté production), **Semantic Kernel** (Microsoft/Azure), ou **fait maison** (plus formateur mais plus long). LlamaIndex est le plus simple pour débuter en RAG.

> Pourquoi Gemini et pas Claude ou GPT ?
→ J'avais déjà des clés API Gemini, le tier gratuit est généreux, et Google propose à la fois des modèles d'embedding ET de génération. Pas besoin de dépenser pour apprendre.

---

## Module 2 — Mon premier RAG

### Concepts clés
- Le script `app.py` suit 5 étapes : configurer l'API → choisir les modèles → indexer les documents → créer le moteur de requêtes → boucle interactive.
- **Deux modèles travaillent ensemble** :
  - Le modèle d'**embedding** (gemini-embedding-001) — transforme le texte en vecteurs. Il catalogue, il ne réfléchit pas.
  - Le modèle de **génération** (gemini-2.5-flash) — lit les morceaux récupérés et rédige la réponse.
- `SimpleDirectoryReader("docs")` — charge tous les fichiers d'un dossier.
- `VectorStoreIndex.from_documents()` — découpe, vectorise et stocke en une seule ligne.
- `index.as_query_engine()` — crée le moteur complet (retrieval + generation).

### Premiers tests et résultats
- Paragraphe de texte → réponse correcte
- Données d'un tableau → extraction correcte
- Liste à puces demandée → bien formaté
- Contenu sous forme d'image dans le PDF → **pas trouvé** (limitation de pypdf qui ne lit pas les images)

### FAQ Apprenant

> Est-ce que gemini-2.0-flash est suffisant ou faut-il un modèle plus puissant ?
→ Dans un RAG, le LLM a un travail simple : lire des extraits et reformuler. Pas besoin d'un modèle premium. Règle d'or : commencer par le moins cher qui fait le job, monter en gamme seulement si les réponses sont insuffisantes.

> Comment choisir le bon modèle ?
→ **Flash/Lite** (gemini-flash, claude-haiku) — RAG basique, résumé, classification. 80% des cas. **Standard** (gemini-pro, claude-sonnet) — analyse complexe, code élaboré. **Premium** (claude-opus) — raisonnement poussé, créativité. Pour du RAG sur des PDFs, Flash suffit.

> J'ai eu une erreur "limit: 0" avec gemini-2.0-flash, c'est quoi ?
→ Google avait désactivé le tier gratuit pour ce modèle. Ce n'est pas une erreur de code, c'est un changement de quota côté Google. Leçon : en production, toujours prévoir un fallback si un modèle devient indisponible.

---

## Module 3 — Sous le capot

### Concepts clés

**Le chunking (découpage) :**
- `chunk_size=1024` — taille d'un morceau en tokens (un token ≈ un mot ou bout de mot).
- `chunk_overlap=200` — chevauchement entre morceaux consécutifs. Les 200 derniers tokens d'un chunk sont aussi les 200 premiers du suivant.
- Le overlap crée un pont entre les chunks — comme photocopier les dernières lignes d'une fiche sur le début de la fiche suivante. Sans ça, on risque de couper un paragraphe en deux et perdre le sens.
- `SentenceSplitter` — le découpeur de LlamaIndex. Il respecte les limites de phrases.

**Le retrieval (recherche) :**
- `index.as_retriever(similarity_top_k=5)` — crée un chercheur qui ramène les 5 morceaux les plus pertinents.
- **Score de similarité** (0 à 1) — distance entre le vecteur de la question et le vecteur du chunk. Plus c'est proche de 1, plus c'est pertinent.
- Différence importante : `retriever` cherche les chunks, `query_engine` cherche ET génère une réponse.

**L'impact des paramètres :**

| Config | Chunks | Avantage | Risque |
|--------|--------|----------|--------|
| Petits (256) | Beaucoup, très ciblés | Scores élevés, précis | Manque de contexte |
| Moyens (1024) | Équilibré | Bon compromis | C'est le défaut pour une raison |
| Gros (2048) | Peu, riches en contexte | Vue d'ensemble | Bruit — info pertinente noyée dans la masse |

### Résultats des expérimentations

**Script 1 — `debug_chunks.py` (visualiser le découpage) :**
- 50 pages chargées → 51 chunks créés (ratio quasi 1:1)
- Taille moyenne : 1358 caractères par chunk
- Les 3 premiers chunks (couverture, sommaire, avant-propos) ne contiennent aucun contenu utile pour un RAG → en production, il faudrait filtrer les pages non pertinentes
- Les warnings `Ignoring wrong pointing object` viennent de pypdf face à des défauts de structure dans les PDFs — ça ne bloque pas la lecture

**Script 2 — `debug_retrieval.py` (voir les scores de similarité) :**

| Question | Scores top 3 | Observation |
|----------|-------------|-------------|
| "qu'est-ce que le RAG ?" | 0.82, 0.79, 0.78 | Scores élevés — contenu directement pertinent |
| "Quelle est la capitale du Brésil ?" | 0.71, 0.68, 0.68 | Scores plus bas (~0.10 d'écart) — aucun contenu pertinent |
| "comment fonctionne la recherche par similarité vectorielle ?" | 0.81, 0.81, 0.80 | Scores élevés — les bons chapitres (pages 9, 10, 11) sont trouvés |

Observations clés :
- Le retriever ramène **toujours** `top_k` résultats, même si rien n'est pertinent. C'est le LLM qui juge ensuite si les chunks permettent de répondre.
- Un score de 0.60-0.70 c'est le "bruit de fond" (même langue, même structure). L'écart avec un vrai résultat pertinent (0.80+) est ce qui compte.
- Les embeddings comprennent le sens, pas juste les mots : "similarité vectorielle" a trouvé les pages sur "représentation vectorielle du sens".

**Script 3 — `debug_params.py` (impact de la taille des chunks) :**

| Config | Chunks créés | Scores top 3 | Réponse |
|--------|-------------|-------------|---------|
| Gros (2048) | 50 | 0.82, 0.81, 0.80 | Complète et correcte |
| Moyens (1024) | 51 | 0.82, 0.81, 0.80 | Complète et correcte |
| Petits (256) | 119 | 0.82, 0.81, 0.80 | Complète et correcte |

Observations clés :
- Les scores sont **identiques** pour les 3 configs — avec un petit corpus (50 pages), le chunking a peu d'impact
- Gros et moyens produisent quasi le même nombre de chunks (50 vs 51) → les pages ne sont pas assez denses pour être découpées davantage
- L'impact du chunking devient critique avec des centaines/milliers de documents, pas avec 50 pages
- Ne pas sur-optimiser les paramètres sur un petit jeu de données

**Erreur rencontrée :** `DeadlineExceeded: 504` avec les petits chunks (256) — l'API Gemini a timeout car trop de chunks à vectoriser d'un coup. Solution : `embed_batch_size=10` pour envoyer les embeddings par petits lots. Leçon : plus les chunks sont petits, plus l'indexation coûte cher en appels API.

### Plan de tests pour évaluer un RAG
1. **Précision du retrieval** — synonymes, détails précis, infos réparties sur plusieurs docs, questions hors sujet (hallucination)
2. **Qualité de la génération** — raisonnement complexe, multilinguisme, comparaisons
3. **Limites du chunking** — réponse à cheval sur deux pages, contexte long
4. **Robustesse** — fautes d'orthographe, ambiguïté, cohérence des réponses
5. **Volume** — plus de documents, temps de réponse

### FAQ Apprenant

> C'est quoi la différence entre retriever et query_engine ?
→ Le `retriever` est le bibliothécaire — il cherche et te ramène les morceaux pertinents. Le `query_engine` c'est le bibliothécaire + le prof — il cherche les morceaux puis les envoie au LLM pour générer une réponse complète.

> Pourquoi un overlap entre les chunks ?
→ Sans overlap, si un concept commence à la fin d'un chunk et se termine au début du suivant, tu le perds. L'overlap garantit que le contexte n'est pas coupé. C'est comme les raccords entre deux photos panoramiques.

> Comment savoir si mon RAG hallucine ?
→ Pose une question dont la réponse n'est pas dans tes documents (ex : "Quelle est la capitale du Brésil ?"). Regarde les scores de similarité en mode debug — s'ils sont tous bas, le RAG a bien cherché mais n'a rien trouvé de pertinent. Un bon RAG le dit honnêtement, un mauvais invente.

> `chunk_size=1024` c'est 1024 caractères ?
→ Non ! C'est 1024 **tokens**. Un token ≈ 3-4 caractères en français. Donc 1024 tokens ≈ 3000-4000 caractères. C'est pour ça qu'on voit des chunks à 1778 caractères qui sont bien en dessous de la limite. Confusion courante : token ≠ caractère.

> Pourquoi le score est à 70% pour une question hors sujet ? Je m'attendais à beaucoup moins.
→ Le score de similarité n'est pas un pourcentage de "bonne réponse". Deux textes en français partagent déjà des caractéristiques (langue, grammaire) qui créent un plancher à 0.60-0.70. C'est l'écart entre les scores qui compte : 0.82 (pertinent) vs 0.71 (hors sujet) = une vraie différence.

> Qui décide qu'il n'y a pas de réponse ? Le score ou le LLM ?
→ Le LLM. Le retriever ramène toujours `top_k` résultats sans juger. C'est le LLM qui lit les chunks et décide "ces extraits ne contiennent pas l'information demandée". Il n'y a pas de seuil de score automatique par défaut — on pourrait en ajouter un, mais c'est une optimisation pour plus tard.

> C'est quoi la différence entre Temperature, Top-K et Top-P ?
→ Attention : le `similarity_top_k` du retriever (combien de chunks chercher) et le `top_k` du LLM (comment choisir les mots) sont deux choses différentes avec le même nom. **Temperature** = niveau de créativité du LLM (0 = déterministe, 1 = audacieux). **Top-K du LLM** = nombre fixe de mots candidats ("choisis parmi les 10 meilleurs"). **Top-P** = nombre adaptatif de candidats ("choisis parmi les mots qui couvrent 90% des probabilités"). Pour un RAG : temperature basse (0-0.3) et top_p autour de 0.8-0.9 — on veut des réponses fidèles, pas de l'improvisation.

---

## Module 4 — Persistance et structure

### Concepts clés

**La persistance :**
- Avant : `VectorStoreIndex.from_documents()` → tout en RAM, perdu à la fermeture. Comme un Google Sheet sans cliquer "Enregistrer".
- Après : **ChromaDB** stocke les vecteurs sur le disque. L'indexation se fait une seule fois, l'interrogation charge depuis le disque.
- `PersistentClient(path="chroma_db")` → les données survivent à l'arrêt du programme.
- `get_or_create_collection("mes_cours")` → une "collection" c'est comme une table BigQuery ou un Drive partagé.
- `VectorStoreIndex.from_vector_store()` → charge depuis le stockage existant (au lieu de `from_documents` qui recrée tout).

**La séparation des responsabilités :**
- `config.py` → configuration centralisée (un seul endroit à modifier)
- `indexer.py` → indexation (on le lance UNE fois, ou quand on ajoute des documents)
- `query.py` → interrogation (on le lance à volonté, chargement instantané)
- Même logique qu'une migration : on migre une fois, on utilise tous les jours.

**Le `.env` pour la clé API :**
- Ne jamais écrire la clé directement dans le code
- `python-dotenv` + fichier `.env` → la clé est dans un fichier séparé, ignoré par Git
- `.gitignore` protège le `.env`, le `venv/`, le `chroma_db/`

### Résultats des expérimentations

- 199 pages → 200 chunks → stockés dans ChromaDB avec succès
- `query.py` charge instantanément depuis le disque — zéro ré-indexation
- Le RAG répond correctement sur un corpus 4x plus grand (200 chunks vs 51 avant)

**Problème de langue :** le RAG répond en anglais par défaut même avec des documents en français. Il faut préciser "répond en français" dans la question. Solution future : ajouter un system prompt au LLM.

**Problème de cohérence :** la même question posée 2 fois donne des réponses légèrement différentes. C'est la temperature du LLM. Solution future : baisser la temperature pour des réponses plus déterministes.

**Problème de doublons :** relancer `indexer.py` sans vider ChromaDB crée des doublons. Solution temporaire : supprimer le dossier `chroma_db/` avant de ré-indexer. Solution propre : à venir dans le cours.

### Erreurs rencontrées et solutions

| Erreur | Cause | Solution |
|--------|-------|----------|
| `DeadlineExceeded: 504` | Trop de chunks envoyés d'un coup à l'API | `embed_batch_size=10` → envoi par lots de 10 |
| `ResourceExhausted: 429` | Quota gratuit épuisé | Activer la facturation Gemini (~0.03€ pour 200 pages) |

### Comprendre les quotas API (RPM, TPM, RPD)

| Sigle | Signification | Ce que ça veut dire |
|-------|--------------|-------------------|
| **RPM** | Requests Per Minute | Combien d'appels API par minute |
| **TPM** | Tokens Per Minute | Combien de tokens par minute |
| **RPD** | Requests Per Day | Combien d'appels API par jour |

Le tier gratuit c'est pour tester, pas pour travailler. Exemples de limites :
- Gemini Embedding gratuit : 418 RPD → payant : **illimité**
- Gemini Flash gratuit : 15 RPD → payant : 10 000 RPD
- Coût réel : ~0.15$ par million de tokens d'embedding. 200 pages = 0.03$.

### FAQ Apprenant

> Pourquoi séparer `indexer.py` et `query.py` ?
→ L'indexation est lourde (lecture des PDFs, découpage, appels API embedding). L'interrogation est légère (charger les vecteurs depuis le disque, un seul appel LLM). Les séparer permet de ne pas refaire le travail lourd à chaque question. C'est comme une migration : on migre une fois, on utilise tous les jours.

> C'est quoi ChromaDB ?
→ Une base de données spécialisée pour stocker des vecteurs. Comme SQLite mais pour des embeddings. Pas de compte à créer, pas de serveur à installer — c'est un package Python qui stocke ses données dans un simple dossier sur ton disque. L'équivalent : imagine un Google Sheet qui tourne en local sur ta machine sans connexion Google, mais optimisé pour la recherche par similarité.

> Est-ce que ChromaDB c'est seulement pour du local / petit volume ?
→ Non. ChromaDB a deux modes : **embarqué** (dans ton script, un seul utilisateur — notre cas) et **serveur** (déployé sur l'infra de l'entreprise, multi-utilisateurs). Une seule ligne de code change : `PersistentClient` → `HttpClient`. Des employés de plusieurs villes peuvent se connecter au même serveur ChromaDB.

> Pour une entreprise, ChromaDB serveur ou Pinecone Cloud ?
→ Ça dépend du besoin. Voici le comparatif :

| Critère | ChromaDB serveur | Pinecone / Weaviate Cloud |
|---------|-----------------|--------------------------|
| Hébergement | Le serveur de l'entreprise | Géré par le fournisseur |
| Maintenance | L'entreprise gère | Le fournisseur s'en occupe |
| Scalabilité | Limitée à la puissance du serveur | S'adapte automatiquement |
| Multi-utilisateurs | Oui, mais basique | Oui, optimisé pour ça |
| Coût | Le coût du serveur uniquement | Abonnement mensuel |
| Données sensibles | **Restent chez le client** | Chez le fournisseur (cloud) |

→ Le dernier point est souvent décisif : si l'entreprise a des données sensibles (contrats, RH, finances), elle préférera ChromaDB sur son propre serveur. Les données ne sortent jamais de leur infrastructure — argument fort avec le RGPD en Europe.

> Quelles sont les alternatives à ChromaDB ?
→ Le paysage des bases vectorielles :

| Base | Type | Analogie |
|------|------|----------|
| **ChromaDB** | Locale ou serveur | SQLite — simple, léger, idéal pour prototyper et PME |
| **Pinecone** | Cloud managé | BigQuery — il faut un compte, c'est payant, ça scale |
| **Weaviate** | Serveur auto-hébergé | MySQL/PostgreSQL — puissant, plus complexe |
| **pgvector** | Extension PostgreSQL | Plugin sur un outil existant |
| **FAISS** (Meta) | Librairie Python pure | Outil de calcul brut, pas une vraie "base de données" |

> Si je change le modèle d'embedding, je dois ré-indexer ?
→ Oui. Chaque modèle d'embedding produit des vecteurs dans son propre "espace". Les vecteurs de Gemini ne sont pas compatibles avec ceux d'OpenAI ou de sentence-transformers. Changer de modèle = tout ré-indexer.

> L'embedding local (gratuit) est-il moins bon que Gemini (payant) ?
→ Pas forcément. Les benchmarks français (MTEB-French) montrent que des modèles open source comme `sentence-camembert-large` rivalisent avec les APIs commerciales. La différence est souvent marginale pour un RAG classique. L'avantage du local : illimité, pas de quota. L'avantage du cloud : plus simple à mettre en place.

> Pourquoi le RAG répond en anglais alors que mes documents sont en français ?
→ Le LLM n'a pas d'instruction de langue par défaut. Il choisit tout seul, souvent l'anglais. En production, on ajoute un "system prompt" qui lui dit : "Réponds toujours en français". On verra ça dans un prochain module.

---

## Suivi de progression

| Module | Statut | Notes |
|--------|--------|-------|
| 0 — Schéma mental | Terminé | Analogie bibliothèque, pipeline entreprise |
| 1 — Setup | Terminé | Python 3.11, venv, packages installés |
| 2 — Premier RAG | Terminé | app.py fonctionnel, premiers tests OK |
| 3 — Sous le capot | Terminé | Scripts debug créés, paramètres testés |
| 4 — Persistance et structure | Terminé | ChromaDB, config.py, indexer/query séparés, tier payant activé |
| 5 — Personnaliser le comportement | Terminé | System prompt, temperature, preprocessing |
| 6 — Interface web (Streamlit) | Terminé | ui.py, cache, session_state, scores L2 vs cosine |
| 7 — RAG multimodal (images) | Terminé | PyMuPDF, Gemini vision, descriptions indexées, 291 chunks |
| 8 — À venir | - | - |

---

## Module 7 — RAG multimodal (images et schémas)

### Concepts clés

**Le problème des images dans un RAG texte :**
- `pypdf` extrait uniquement la couche texte d'un PDF. Un schéma inséré comme image n'a pas de couche texte — pour pypdf, c'est un rectangle vide.
- Analogie : un tableau Excel construit avec des cellules et formules, tu peux le migrer vers Sheets. Un tableau qui est une capture d'écran collée dans Excel ? Impossible à convertir automatiquement.

**Les trois stratégies possibles :**

| Stratégie | Méthode | Forces | Limites |
|-----------|---------|--------|---------|
| **OCR** (Tesseract) | Reconnaissance de caractères sur l'image | Gratuit, open source | Mauvais sur schémas complexes, texte manuscrit |
| **LLM multimodal** | Envoyer l'image à un modèle qui "voit" (Gemini) | Comprend les schémas, diagrammes, graphiques | Coût API par image |
| **Extraction spécialisée** (Camelot, Tabula) | Outils dédiés aux tableaux en image | Très précis pour les tableaux | Limité aux tableaux uniquement |

**Notre choix : Stratégie 2 — LLM multimodal (Gemini).**
- Gemini est multimodal nativement — il accepte les images en entrée.
- On extrait les images avec PyMuPDF, on les envoie à Gemini, il les décrit en français.
- Les descriptions textuelles sont sauvegardées en `.txt` dans `docs/` et indexées normalement.
- Élégance : les images deviennent du texte, le texte entre dans le pipeline RAG standard. Pas besoin de modifier l'architecture.

**Les outils :**

| Outil | Rôle |
|-------|------|
| **PyMuPDF** (`fitz`) | Extraction d'images depuis les PDFs (plus puissant que pypdf) |
| **Pillow** (PIL) | Manipulation d'images (taille, format) |
| **google-generativeai** | SDK Gemini pour envoyer les images au modèle |

**Le filtre par taille (150x150 pixels minimum) :**
- Les PDFs contiennent beaucoup de micro-images : icônes, puces, décorations visuelles.
- On ne garde que les images > 150x150 pixels — suffisamment grandes pour être des schémas utiles.
- Même logique que le filtre de preprocessing (leçon 5) : retirer le bruit avant d'indexer.

**Le workflow multimodal :**
```
python extract_images.py  → Extraire et décrire les images (une fois)
python indexer.py          → Ré-indexer avec les descriptions en plus
python -m streamlit run ui.py → Utiliser le RAG enrichi
```

### Résultats des expérimentations

**Extraction des images :**

| PDF | Images significatives | Descriptions générées |
|-----|----------------------|----------------------|
| RAG_La_Verite_Derriere_La_Promesse.pdf | 17 | 17 (254 à 6921 chars) |
| Cours sur l'IA (3).pdf | 30 | 30 (1510 à 3879 chars) |
| Manuel_IA_FINAL (1).pdf | 18 | 18 (2407 à 6685 chars) |
| Guide_RAG.pdf | 10 | 10 (3115 à 6936 chars) |
| Guide-Orchestration-IA-3.pdf | 0 | — (texte pur) |
| Naviguer_la_Revolution_IA.pdf | 0 | — (texte pur) |
| **Total** | **75** | **75 (zéro erreur)** |

**Impact sur l'index :**

| Métrique | Avant (texte seul) | Après (multimodal) |
|----------|-------------------|-------------------|
| Pages chargées | 199 | 262 (+75 descriptions) |
| Pages retenues | 189 | 252 |
| Chunks indexés | 190 | **291** (+101 chunks) |

**Test de validation — questions sur un schéma en image :**

Le schéma "Comment schématiser un RAG?" (pipeline complet avec Ingénierie des Données / Génération Augmentée) était invisible pour le RAG en texte seul. Après l'extraction multimodale :

| Question | Réponse correcte ? | Sources `IMG_DESC_` ? |
|----------|--------------------|-----------------------|
| "Quelles sont les étapes de l'ingénierie des données dans un pipeline RAG ?" | Oui — 4 étapes détaillées | Oui (score 0.71) |
| "Quelle est la différence entre le socle et le flux dans un système RAG ?" | Oui — distinction claire | Oui (score 0.60) |
| "Que signifie 'La qualité ici détermine la fiabilité du reste' ?" | Oui — explication contextualisée | Oui (score 0.65) |

→ 100% des réponses proviennent des descriptions d'images. La question piège (texte écrit en bas d'un schéma, uniquement dans les pixels) a été retrouvée grâce à la description de Gemini.

### FAQ Apprenant

> Pourquoi pypdf ne voit pas les images ?
→ Un PDF est un mille-feuille de couches : texte, mise en page, images. `pypdf` ne lit que la couche texte. Un schéma inséré comme image n'a pas de texte — c'est des pixels. Il faut un outil spécialisé (PyMuPDF) pour extraire ces pixels, puis un modèle multimodal (Gemini) pour les "lire".

> Est-ce que ça coûte cher d'envoyer 75 images à Gemini ?
→ Gemini facture les images en tokens (une image ≈ quelques centaines de tokens). Pour 75 images avec Gemini Flash, c'est quelques centimes. Négligeable par rapport au coût de l'embedding. Et c'est fait une seule fois — les descriptions sont ensuite indexées comme du texte.

> Pourquoi filtrer les images < 150x150 pixels ?
→ Les PDFs contiennent des dizaines de micro-images : icônes de navigation, puces décoratives, logos minuscules. Les envoyer à Gemini gaspille de l'API pour des descriptions inutiles ("cette image montre une petite icône ronde"). Le filtre 150x150 ne garde que les schémas, graphiques et tableaux significatifs.

> Les descriptions d'images sont-elles aussi bonnes que le vrai texte ?
→ Elles sont différentes. Gemini interprète et décrit — il ne retranscrit pas mot pour mot. Pour un schéma d'architecture, la description est souvent plus explicite que le texte original (elle nomme chaque élément et ses relations). Pour un graphique avec des chiffres précis, elle peut perdre en exactitude. C'est un compromis : mieux qu'un trou dans l'index, moins parfait qu'un texte natif.

---

## Module 6 — Rendre le RAG présentable (Interface web)

### Concepts clés

**Streamlit :**
- Framework Python qui transforme un script en application web en quelques lignes.
- Pas besoin de HTML/CSS/JS — tout se fait en Python.
- Analogie : c'est le Google Sites du développeur Python — ça rend un truc technique accessible à n'importe qui.
- Lancement : `python -m streamlit run ui.py` (utiliser `python -m` pour rester dans le venv).

**Les composants Streamlit utilisés :**

| Composant | Rôle | Analogie |
|-----------|------|----------|
| `st.chat_input` / `st.chat_message` | Interface de chat | WhatsApp / ChatGPT |
| `st.sidebar` | Panneau latéral avec infos et paramètres | Le panneau de réglages d'une app |
| `st.slider` | Réglage interactif (top_k) | Le client ajuste sans toucher au code |
| `st.expander` | Contenu dépliable (sources) | Les détails masqués par défaut |
| `st.metric` | Affichage de métriques | Le dashboard d'un outil de monitoring |
| `st.spinner` | Indicateur de chargement | "Patience, je cherche..." |

**`@st.cache_resource` — Le cache :**
- Charge l'index ChromaDB **une seule fois**, même si l'utilisateur rafraîchit la page ou pose 50 questions.
- Sans cache, chaque question rechargerait ChromaDB depuis le disque.
- Même principe que la persistance (leçon 4), mais au niveau de la session web.

**`st.session_state` — La mémoire de conversation :**
- Stocke l'historique des messages pendant la session.
- Sans ça, chaque nouvelle question effacerait les précédentes.
- En production, cette mémoire serait stockée dans une base de données pour survivre entre les sessions.

**Les sources sous chaque réponse :**
- Crucial en entreprise — un directeur ne fait pas confiance à une IA sans traçabilité.
- Chaque réponse montre : le fichier source, la page, le score de pertinence, et un extrait.
- C'est ce qui fait la différence entre un gadget et un outil professionnel.

### Résultats des expérimentations

- Interface fonctionnelle sur `http://localhost:8501`
- Chat interactif avec historique de conversation
- Sidebar avec métriques (190 chunks, gemini-2.5-flash, temperature 0.1)
- Slider top_k ajustable en temps réel par l'utilisateur
- Sources consultées affichées sous chaque réponse

**Observation importante — Baisse des scores de similarité :**

| Test | Avant (debug_retrieval.py) | Maintenant (ui.py) |
|------|---------------------------|-------------------|
| Question pertinente | ~0.80 | ~0.64 |
| "Capitale du Brésil" (hors sujet) | ~0.70 | ~0.54 |
| Écart pertinent vs hors sujet | ~0.10 | ~0.10 |

**Explication :** ce n'est pas une dégradation. Le moteur de calcul a changé. L'index en mémoire (leçons 1-3) utilisait la **similarité cosinus** (échelle ~0.60-0.85). ChromaDB utilise par défaut la **distance euclidienne L2** (échelle ~0.50-0.65). C'est comme Celsius vs Fahrenheit — les chiffres sont différents, la mesure est équivalente. Ce qui compte : l'écart relatif est **préservé**. Le retrieval fonctionne aussi bien.

**Test du system prompt via l'interface :**
- "Quelle est la capitale du Brésil" → "Je ne dispose pas d'informations sur la capitale du Brésil dans le contexte fourni." — **en français**, refus poli, sources affichées. Le system prompt fonctionne.

### Erreurs rencontrées et solutions

| Erreur | Cause | Solution |
|--------|-------|----------|
| `ModuleNotFoundError: No module named 'llama_index'` | `streamlit run` utilisait le Python système (Homebrew) au lieu du venv | Utiliser `python -m streamlit run ui.py` pour forcer le Python du venv |

### FAQ Apprenant

> Pourquoi `python -m streamlit run` au lieu de `streamlit run` ?
→ Quand tu tapes `streamlit run`, ton terminal cherche la commande `streamlit` dans le PATH. S'il en trouve une installée au niveau système (Homebrew), il l'utilise — et ce Python système ne connaît pas tes packages venv. `python -m streamlit` force l'utilisation du Python actif (celui du venv), qui a accès à tous tes packages.

> Pourquoi les scores sont plus bas qu'avant avec ChromaDB ?
→ Les scores ne sont pas comparables entre les deux systèmes. L'index en mémoire utilisait la similarité cosinus (0 à 1), ChromaDB utilise la distance euclidienne L2 par défaut. Les chiffres sont différents mais le classement est le même — les chunks pertinents restent en haut. C'est l'écart relatif entre les scores qui fait le travail, pas la valeur absolue.

> C'est quoi `@st.cache_resource` ?
→ Un décorateur qui dit à Streamlit : "exécute cette fonction une seule fois et garde le résultat en mémoire". Chaque nouvelle question réutilise l'index déjà chargé au lieu de relire ChromaDB. Sans ça, chaque interaction rechargerait tout — comme si tu rouvrais un fichier Excel à chaque cellule modifiée.

> C'est quoi `st.session_state` ?
→ Un dictionnaire qui persiste pendant toute la session utilisateur. On y stocke l'historique des messages. Sans ça, Streamlit ré-exécute tout le script à chaque interaction et l'historique disparaît. C'est la mémoire à court terme de ton app web.

---

## Module 5 — Personnaliser le comportement du RAG

### Concepts clés

**Le System Prompt :**
- Instruction invisible envoyée au LLM avant chaque requête. L'utilisateur ne la voit pas.
- C'est le brief qu'on donne à un consultant avant une mission : "tu es poli, tu parles français, tu ne sors pas du périmètre, tu cites tes sources."
- Défini dans `config.py`, branché sur le `query_engine` via le paramètre `system_prompt=`.
- ⚠️ Un system prompt est une **directive, pas une obligation**. Le LLM essaie de la suivre, mais il peut être influencé par d'autres facteurs (langue du contenu récupéré, formulation de la question).

**La Temperature :**
- Contrôle le niveau de "créativité" du LLM lors de la génération.
- `0.0` = déterministe (même question → même réponse à chaque fois)
- `0.1` = quasi déterministe — notre choix pour un RAG factuel
- `0.7` = défaut chez la plupart des LLMs — variabilité notable
- `1.0` = très créatif — risque d'hallucination accru
- **Règle d'or :** RAG factuel → temperature basse (0.0-0.2). Chatbot créatif → temperature haute. En entreprise, documentation interne = toujours 0.0 à 0.2.

**Le Preprocessing (filtrage des pages) :**
- Avant d'indexer, on retire les pages qui n'apportent aucune valeur au RAG.
- Deux stratégies complémentaires :
  1. **Filtre par taille** — pages < 100 caractères = probablement couvertures, pages blanches, titres seuls
  2. **Filtre par mots-clés** — pages dont le début contient "sommaire", "table des matières", etc.
- **Bonne pratique validée** : les tables des matières ne doivent **pas** être indexées comme du contenu. Elles créent du bruit — elles matchent beaucoup de requêtes sans apporter de réponse utile. En approche avancée, on peut les convertir en métadonnées pour enrichir les chunks (hors scope pour l'instant).
- Attention : un filtre trop agressif est pire que pas de filtre. **Toujours vérifier** les pages supprimées avant d'appliquer.

### Résultats des expérimentations

**System Prompt :**

| Test | Instruction "en français" dans la question ? | Réponse en français ? |
|------|----------------------------------------------|----------------------|
| Question créative, ton très français | Non | Oui |
| Question factuelle standard | Non | **Non — anglais** |
| Même question + "Répond en français" | Oui | Oui |

→ Le system prompt aide mais ne garantit pas à 100% la langue de réponse. Gemini peut être influencé par le contenu des chunks récupérés. À ajuster en production (system prompt plus insistant, instruction dans la requête elle-même).

**Preprocessing :**
- 199 pages chargées → **189 pages retenues** (10 supprimées)
- Pages supprimées : 6 titres de sections, 1 page quasi vide, 2 tables des matières/sommaires, 1 page-image (schéma RAG)
- 190 chunks indexés au lieu de 200 → 10 chunks de bruit en moins dans le retrieval
- Bug corrigé en cours de route : le filtre par mots-clés vérifiait la taille totale de la page (`len < 300`) au lieu de chercher le mot-clé dans le début. Une table des matières longue passait entre les mailles. Corrigé en vérifiant les 300 premiers caractères.

### FAQ Apprenant

> C'est quoi un system prompt ?
→ Une instruction invisible que l'utilisateur final ne voit jamais. C'est le cadrage du LLM : sa langue, sa personnalité, ses interdictions, son style de réponse. Sans system prompt, le LLM fait ce qu'il veut. Avec, il suit (en général) les règles qu'on lui donne. Analogie : c'est la fiche de poste du consultant avant sa première journée chez le client.

> Pourquoi mettre la temperature à 0.1 et pas 0 ?
→ À 0.0, le modèle est 100% déterministe mais peut parfois "se bloquer" sur un mauvais chemin de raisonnement. À 0.1, on laisse une micro-marge de manœuvre. C'est le standard pour du RAG factuel — réponses stables sans être rigides.

> Est-ce qu'il faut toujours retirer les tables des matières ?
→ En tant que contenu indexé, oui. Une table des matières matche beaucoup de requêtes (elle mentionne tous les sujets du document) mais ne contient aucune réponse utile. Elle gaspille un slot dans les `top_k` résultats. En approche avancée, on peut la convertir en métadonnées pour enrichir les autres chunks — mais c'est un niveau au-dessus.

> Le system prompt ne marche pas à 100% pour forcer la langue, c'est normal ?
→ Oui. Un system prompt est une directive "souple" — le LLM essaie de la respecter mais peut être influencé par d'autres facteurs : la langue du contenu récupéré, la formulation de la question, ou ses propres biais. Pour renforcer : system prompt plus strict, instruction répétée dans la requête, ou post-traitement de la réponse. En production, on combine plusieurs mécanismes.
