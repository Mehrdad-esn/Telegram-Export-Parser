# 🚀 Telegram Export Parser

> Advanced Telegram chat export processor with multi-service SaaS-ready architecture (frontend + backend + worker)

**Convert Telegram exports (JSON) to multiple formats with advanced analysis, filtering, and visualization.**

---

## 📋 Overview

Telegram Export Parser is a professional-grade tool for processing, analyzing, and exporting Telegram chat data. It features a modern, responsive Next.js frontend, a FastAPI backend with integrated JWT authentication and Stripe subscriptions, a background worker for parsing large payloads, and a robust CLI toolkit.

**Key Capabilities:**
- 📊 **Interactive Analytics** - View message count trends, daily averages, character metrics, top talkers, and word frequencies.
- 🎯 **Powerful Filtering** - Chainable filters by date, sender, keywords, regular expressions (Regex), message length, and media types.
- 📁 **Multi-format Export** - Export processed chats to TXT, CSV, JSON, HTML, Markdown, and styled Excel (XLSX).
- 🔒 **Security First** - In-memory local processing so your personal data never leaves the server.
- 💳 **SaaS Ready** - Fully integrated with Stripe billing checkouts and webhook handlers.
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
│  • Celery/RQ workers for large files                    │
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
│   │   └── routers/               # Route definitions (e.g. web upload)
│   ├── tests/                     # Backend test suite (pytest)
│   ├── requirements.txt           # Python backend dependencies
│   └── Dockerfile                 # Backend container definition
│
├── docker-compose.yml             # Orchestration for frontend + backend + database
├── app.py                         # CLI tool core
├── web_ui.py                      # Flask fallback web application (Port 5000)
├── README.md                      # This file
├── GUIDE.md                       # Developer & Deployment guide
└── SUMMARY_FA.md                  # Persian project summary (گزارش پروژه)
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
|---|---|---|
| `DEBUG` | Enable debug logs | `True` |
| `ENVIRONMENT` | Target environment name | `development` |
| `DATABASE_URL` | SQLAlchemy connection string | `sqlite:///./telegram_export.db` |
| `SECRET_KEY` | JWT signing secret key | *Generate a strong key* |
| `SENTRY_DSN` | Sentry exception DSN | *(Optional)* |

---

**Version:** 2.1.0  
**Status:** ✅ Production Ready  
**Last Updated:** June 2026  
