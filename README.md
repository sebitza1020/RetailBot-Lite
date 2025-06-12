# RetailBot-Lite

Lightweight AI chatbot for retail catalog & FAQ, powered by retrieval‑augmented generation (RAG). Provides real‑time product search, stock availability and instant answers to customer questions — deployable in minutes.

# ✨ Features

- 🔍 Semantic product search across a local CSV catalog, ranked by relevance.
- 📦 Real‑time stock checks via optional inventory API integration.
- 💬 FAQ retrieval from Markdown knowledge base (policies, shipping, returns, etc.).
- 🧠 LLM answers with RAG for factual, referenced responses.
- 📈 Metrics endpoint for answer success‑rate & latency.
- 🐳 One‑command Docker deployment for effortless demo.

# 🚀 Quick demo

```
git clone https://github.com/<you>/retailbot‑lite.git
cd retailbot‑lite
python -m retailbot.chatbot "Do you offer express shipping?"

# Or launch the Flask store demo
python ecommerce/app.py
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

Command line interface & Flask demo

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
 Command line & Flask demo <──────┘                  │
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
3. Run the chatbot or demo store
```
python -m retailbot.chatbot "What are your shipping options?"
# or
python ecommerce/app.py
```
# 📂 Folder structure
```
retailbot-lite/
├─ retailbot/            # chatbot logic
├─ ecommerce/            # Flask demo
├─ data/                 # product_catalog.csv
├─ faq/                  # markdown knowledge base
├─ requirements.txt
└─ README.md
```
# 🧪 Testing
```
pytest
```

## 📟 Command line chatbot

A minimal example using the built‑in CSV catalog and markdown FAQ is provided in
`retailbot/chatbot.py`. Set your `OPENAI_API_KEY` environment variable and ask a
question directly from the terminal:

```bash
python -m retailbot.chatbot "Do you offer express shipping?"
```

The script retrieves relevant products and FAQ entries with semantic search and
uses an LLM to generate the final answer.

## 🛍 Simple Flask store demo

The `ecommerce` folder contains a lightweight shopping cart example powered by
Flask and SQLite. The database is automatically created on first run with sample
products and images.

Run it locally:

```bash
python ecommerce/app.py
```
Open http://localhost:5000 to browse the catalog.
# 🛣️ Roadmap

- Multilingual support (ES, FR, RO)

- Voice interface via WebRTC

- Swappable local embeddings (all‑MiniLM) for offline mode
