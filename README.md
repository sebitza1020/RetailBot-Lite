# RetailBot-Lite

Lightweight AI chatbot for retail catalog & FAQ, powered by retrieval‑augmented generation (RAG). Provides real‑time product search, stock availability and instant answers to customer questions — deployable in minutes.

# ✨ Features

- 🔍 Semantic product search across a local CSV catalog, ranked by relevance.
- 📦 Real‑time stock checks via optional inventory API integration.
- 💬 FAQ retrieval from Markdown knowledge base (policies, shipping, returns, etc.).
- 🧠 LLM answers with RAG for factual, referenced responses.
- 📈 Metrics endpoint for answer success‑rate & latency.
- 🐳 One‑command Docker deployment for effortless demo.

# 🚀 Quick demo (Docker)

```
git clone https://github.com/<you>/retailbot‑lite.git
cd retailbot‑lite
docker compose up --build
# open http://localhost:8501 in your browser
```

# 🛠️ Tech stack

Layer

Library / Service

API

FastAPI

Embeddings

OpenAI Ada v2 (configurable)

Retrieval

FAISS (in‑memory)

Orchestration

LangChain

UI

Streamlit

Container

Docker, docker‑compose

# 🏗️ Architecture

```
(.md) FAQ  ─┐
            ▼            ┌────────┐
(.csv) Catalog ──> Vector Store ──>│  LLM   │
                                   └────────┘
     ▲                ▲                  ▲
     │ REST API       │ embeddings       │
 Streamlit UI <───────┘                  │
                                     External
                                    Inventory API
```

# ⚙️ Getting started (local)

1. Clone & create venv
```
git clone https://github.com/<you>/retailbot‑lite.git
cd retailbot‑lite
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
2. Configure env vars
```
cp .env.example .env
# edit OPENAI_API_KEY, CATALOG_PATH, etc.
```
3. Run services
```
uvicorn app.main:app --reload      # REST API at :8000
streamlit run ui/app.py            # Chat UI at :8501
```
# 📂 Folder structure
```
retailbot‑lite/
├─ app/
│  ├─ api/            # FastAPI routes
│  ├─ core/           # settings, logger, schemas
│  ├─ services/       # embedding & search logic
│  └─ faq/            # markdown knowledge base
├─ data/              # product_catalog.csv
├─ ui/                # Streamlit frontend
├─ tests/
├─ docker-compose.yml
└─ README.md
```
# 🧪 Testing
```
pytest
```
# 🛣️ Roadmap

- Multilingual support (ES, FR, RO)

- Voice interface via WebRTC

- Swappable local embeddings (all‑MiniLM) for offline mode
