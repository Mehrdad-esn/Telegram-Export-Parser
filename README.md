# 🚀 Telegram Export Parser

> Telegram chat export processor with multi-service architecture (frontend + backend + worker)

**Convert Telegram exports (JSON) to multiple formats with advanced analysis, filtering, and visualization.**

---

## 📋 Overview

Telegram Export Parser is a tool for processing, analyzing, and exporting Telegram chat data. It features a modern, responsive Next.js frontend, a FastAPI backend with integrated JWT authentication and Stripe subscriptions, a background worker for parsing large payloads, and a robust CLI toolkit.

**Key Capabilities:**
- 📊 **Interactive Analytics** - View message count trends, daily averages, character metrics, top talkers, and word frequencies.
- 🎯 **Powerful Filtering** - Chainable filters by date, sender, keywords, regular expressions (Regex), message length, and media types.
- 📁 **Multi-format Export** - Export processed chats to TXT, CSV, JSON, HTML, Markdown, and styled Excel (XLSX).
- 🔒 **Security First** - In-memory local processing so your personal data never leaves the server.
- 💳 **Stripe Integration** - Stripe billing checkouts and webhook handlers (free plans for now).
- 📈 **System Monitoring** - Out-of-the-box Prometheus metrics (`/metrics`) and Sentry error tracking.
- 🐳 **Dockerized Setup** - Run the entire multi-service stack with a single command.

---

## 🏗️ Architecture

### Multi-Service Setup

```
┌─────────────────────────────────────────────────────────┐
│                    Web Browser                          │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST
┌────────────────────▼────────────────────────────────────┐
│  Frontend Service (Next.js + TypeScript + Tailwind)    │
│  • Dashboard analytics (Recharts)                       │
│  • Live chat list & format selection                    │
│  • Stripe Pricing pages & JWT Auth forms                │
│  Port: 3000                                             │
└────────────────────┬────────────────────────────────────┘
                     │ API Calls (http://localhost:8000)
┌────────────────────▼────────────────────────────────────┐
│  Backend Service (FastAPI + Python)                     │
│  • JSON parsing & stats processors                      │
│  • JWT Authentication & SQLite database                  │
│  • Stripe billing API & webhooks                        │
│  • Prometheus metrics & Sentry logging                  │
│  Port: 8000                                             │
└────────────────────┬────────────────────────────────────┘
                     │ (Optional Redis Queue)
┌────────────────────▼────────────────────────────────────┐
│  Worker & Data Layer                                    │
│  • Celery workers for large files                       │
│  • In-memory stream parser (ijson)                      │
└─────────────────────────────────────────────────────────┘
```

### Directory Structure

```
Telegram Export Parser/
├── frontend/                      # Next.js frontend (Port 3000)
│   ├── pages/                     # Page views (dashboard, auth, pricing, index)
│   ├── components/                # UI widgets & interactive graphs (Recharts)
│   ├── styles/                    # Tailwind CSS configuration
│   ├── Dockerfile                 # Frontend container definition
│   └── package.json               # Node.js dependencies
│
├── backend/                       # FastAPI backend (Port 8000)
│   ├── app/
│   │   ├── main.py                # FastAPI entry point & metrics middleware
│   │   ├── auth.py                # JWT Auth routes & password hashing
│   │   ├── billing.py             # Stripe customer sessions & webhook listeners
│   │   ├── db.py & models.py      # SQLite database engine & user models
│   │   ├── monitoring.py          # Sentry & Prometheus initializations
│   │   ├── processor.py           # Core payload parser wrapper
│   │   ├── routers/               # Route definitions (e.g. web upload)
│   │   └── tasks.py               # Background Celery tasks
│   ├── tests/                     # Backend test suite (pytest)
│   ├── worker.py                  # Celery worker configuration
│   ├── requirements.txt           # Python backend dependencies
│   └── Dockerfile                 # Backend container definition
│
├── templates/                     # Flask web UI template
│   └── index.html
├── .github/workflows/             # CI/CD pipeline
├── docker-compose.yml             # Orchestration for 4 services
├── app.py                         # CLI tool core
├── web_ui.py                      # Flask fallback web application
├── config.py                      # Configuration management
├── exporters.py                   # Multi-format export engines
├── filters.py                     # Message filtering system
├── stats.py                       # Statistics module
├── utils.py                       # Helper utilities
├── telegram_to_text.py            # Core parser
├── examples.py                    # Usage examples
├── test_data.json                 # Sample test data
├── requirements.txt               # Root Python dependencies
├── pyproject.toml                 # Package metadata
├── Dockerfile                     # Legacy Flask container
├── run.bat                        # Windows launcher (all services)
├── run-backend.bat                # Windows backend runner
├── run-frontend.bat               # Windows frontend runner
├── .env.example                   # Environment variable template
├── .pre-commit-config.yaml        # Pre-commit hooks config
└── README.md                      # This file
```

---

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

Start the full local stack (frontend, backend) inside containers:

```bash
# Clone the repository
git clone <repo-url>
cd Telegram-Export-Parser

# Start all services with hot-reload enabled
docker-compose up -d --build

# View container logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop and tear down containers
docker-compose down -v
```

Services:
- **Frontend Panel**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`
- **Swagger Documentation**: `http://localhost:8000/docs`

---

### Option 2: Manual Setup (Local Development)

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
cd frontend
npm install

# Run Next.js dev server
npm run dev
```
Open `http://localhost:3000` in your browser. Next.js is preconfigured to rewrite API calls directly to port `8000`.

---

## 🧪 Testing

```bash
# Run backend tests
cd backend
pytest

# Run frontend tests
cd frontend
npm run test
```

---

## 📁 Feature Roadmap

**Phase 1: Core Parsing Engine** ✅
- Multi-format exporters (TXT, CSV, JSON, HTML, Markdown, XLSX)
- 5+ filter systems (date range, user, keywords, regex, length)
- Message statistics module

**Phase 2: Legacy Interfaces** ✅
- Command Line Interface (CLI) execution with argument parsing
- Flask-based upload UI (port 5000)

**Phase 3: Backend API Service** ✅
- FastAPI integration
- SQLite Database & User Auth (JWT token validation)
- Stripe payments & webhooks integration
- Sentry and Prometheus monitoring

**Phase 4: Modern Front-end Portal** ✅
- Next.js dashboard with dark mode UI
- Recharts visualizations
- Authentication screens and Pricing structures

**Phase 5: Advanced Intelligence** 🚧
- [ ] Auto-translation (AI-based translation of exports)
- [ ] Sentiment Analysis (Emotional classification of chats over time)
- [ ] Interactive User Network Graphs
- [ ] Multi-region Cloud deployments

---

## 🔒 Secrets & Environment Configuration

Copy the template to customize your setup:
```bash
cp .env.example .env
```

| Variable | Description | Default |
|---|---|---|---|
| `DATABASE_URL` | SQLAlchemy connection string | `sqlite:///./telegram_export.db` |
| `SECRET_KEY` | JWT signing secret key | *Generate a strong key* |
| `STRIPE_API_KEY` | Stripe secret key | *(Optional)* |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook signing secret | *(Optional)* |
| `SENTRY_DSN` | Sentry error tracking DSN | *(Optional)* |
| `ENV` | Environment name (development/production) | `development` |
| `APP_VERSION` | Release version for Sentry tracking | `unknown` |
| `REDIS_URL` | Redis connection string for Celery | `redis://localhost:6379/0` |
| `FRONTEND_URL` | Frontend URL for redirects | `http://localhost:3000` |

---

**Version:** 2.0.0  
**Status:** ✅ Development / Learning Project  
**Last Updated:** June 2026  
