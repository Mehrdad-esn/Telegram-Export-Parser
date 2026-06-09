# 🚀 Telegram Export Parser

> Advanced Telegram chat export processor with multi-service architecture (frontend + backend)

**Convert Telegram exports (JSON) to multiple formats with advanced analysis and filtering.**

## 📋 Overview

Telegram Export Parser is a professional-grade tool for processing, analyzing, and exporting Telegram chat data. It features a modern Next.js frontend, FastAPI backend, and comprehensive CLI for batch processing.

**Key Capabilities:**
- 📊 Advanced statistics & sentiment analysis
- 🎯 Powerful filtering (date, user, keywords, regex, media)
- 📁 Multi-format export (TXT, CSV, JSON, HTML, Markdown, Excel)
- 🌐 Web UI for interactive processing
- ⚙️ Extensible plugin architecture
- 🔒 Local processing (no data leaves your machine)

## 🏗️ Architecture

### Multi-Service Setup

```
┌─────────────────────────────────────────────────────────┐
│                    Web Browser                          │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST
┌────────────────────▼────────────────────────────────────┐
│  Frontend Service (Next.js + TypeScript + Tailwind)    │
│  • File upload UI                                       │
│  • Interactive chat preview                            │
│  • Export format selection                             │
│  • Statistics visualization                            │
│  Port: 3000                                            │
└────────────────────┬────────────────────────────────────┘
                     │ API Calls (http://localhost:8000)
┌────────────────────▼────────────────────────────────────┐
│  Backend Service (FastAPI + Python)                     │
│  • File processing & parsing                           │
│  • Advanced filtering                                  │
│  • Statistics calculation                              │
│  • Multi-format export                                 │
│  • Webhook support                                     │
│  Port: 8000                                            │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│  Data Layer                                             │
│  • In-memory processing                                │
│  • SQLite (optional)                                   │
└─────────────────────────────────────────────────────────┘
```

### Directory Structure

```
Telegram Export Parser/
├── frontend/                      # Next.js frontend (Port 3000)
│   ├── pages/                     # React pages
│   ├── components/                # Reusable components
│   ├── styles/                    # Tailwind CSS
│   ├── package.json
│   └── next.config.js
│
├── backend/                       # FastAPI backend (Port 8000)
│   ├── app/
│   │   ├── main.py               # FastAPI entry point
│   │   ├── routers/              # API endpoints
│   │   ├── models/               # Data models
│   │   └── services/             # Business logic
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml             # Local dev orchestration
├── Dockerfile                     # Root-level fallback
├── README.md                      # This file
├── GUIDE.md                       # Developer guide
└── QUICKSTART.sh                  # Quick reference

## ✨ Key Features

### 📊 Statistics & Analysis
- Message count & timeline analysis
- Per-user statistics
- Word frequency analysis
- Average message metrics
- Top talkers ranking
- Sentiment analysis (roadmap)

### 🎯 Advanced Filtering
- Date range filtering (--from-date, --to-date)
- Sender/user filtering
- Keyword search with regex support
- Message length filtering
- Media type filtering
- Chainable filter API

### 📁 Export Formats
- **TXT** - Plain text with formatting
- **CSV** - Excel/Sheets compatible
- **JSON** - Structured data (APIs)
- **HTML** - Web viewable
- **Markdown** - Git-friendly docs
- **XLSX** - Excel with formatting

### 🌐 Multiple Interfaces
- **Web UI** (Next.js) - Drag-drop upload, real-time preview
- **REST API** (FastAPI) - Programmatic access
- **CLI** (Python) - Batch processing
- **Python SDK** - Custom workflows

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose (recommended)
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)

### Option 1: Docker Compose (Recommended)

```bash
# Clone repository
git clone <repo-url>
cd Telegram\ Export\ Parser

# Start all services
docker-compose up --build

# Services will be available at:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup (Local Development)

#### Backend Setup
```bash
# 1. Install backend dependencies
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Run backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# API will be at http://localhost:8000
```

#### Frontend Setup
```bash
# 1. Install frontend dependencies
cd frontend
npm install

# 2. Run development server
npm run dev
# Frontend will be at http://localhost:3000
```

---

## 💻 Local Development

### Starting Services

**Using Docker Compose (all-in-one):**
```bash
docker-compose up
```

**Individually:**
```bash
# Terminal 1: Backend
cd backend && uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend && npm run dev
```

### API Documentation

Once backend is running, view interactive docs:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test
```

### Building for Production

**Backend:**
```bash
docker build -t telegram-export-backend -f backend/Dockerfile backend
docker run -p 8000:8000 telegram-export-backend
```

**Frontend:**
```bash
cd frontend
npm run build
npm start
```

---

## 📋 Docker Compose Configuration

The `docker-compose.yml` includes:

```yaml
services:
  backend:
    - FastAPI on port 8000
    - Volume mount for source code (hot reload)
    - Environment: development
  
  frontend:
    - Next.js on port 3000
    - Volume mount for source code
    - Environment: development
```

**To customize:**
- Edit `docker-compose.yml` for port/env changes
- Use `.env` file for secrets
- Add services (PostgreSQL, Redis) as needed

---

## 🧪 Testing

### Run All Tests
```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm run test
```

### Coverage Report
```bash
# Backend
cd backend && pytest --cov=app tests/
```

---

## 📁 Feature Roadmap

**Phase 1: Core** ✅
- Multi-format export (TXT, CSV, JSON, HTML, MD, XLSX)
- Advanced filtering
- Statistics & analysis

**Phase 2: Web UI** ✅
- Next.js + TypeScript frontend
- Drag-drop file upload
- Real-time chat preview

**Phase 3: API** ✅
- FastAPI backend
- REST endpoints
- Swagger/ReDoc documentation

**Phase 4: Advanced** 🚧
- Sentiment analysis
- Auto-translation
- Database storage (SQLite/PostgreSQL)
- Real-time monitoring dashboard

**Phase 5: Deployment** 🚧
- GitHub Actions CI/CD
- Vercel frontend deployment
- Cloud Run/ECS backend deployment

---

## 🤝 Contributing

### Setup Development Environment

1. **Fork & clone repository**
   ```bash
   git clone <your-fork-url>
   cd Telegram\ Export\ Parser
   ```

2. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature
   ```

3. **Start services**
   ```bash
   docker-compose up
   ```

4. **Make changes** - Edit code in `frontend/` or `backend/`

5. **Run tests**
   ```bash
   # Backend
   cd backend && pytest
   
   # Frontend
   cd frontend && npm run test
   ```

6. **Commit & push**
   ```bash
   git add .
   git commit -m "feat: describe your changes"
   git push origin feature/your-feature
   ```

7. **Create Pull Request** on GitHub

### Code Style

- **Backend**: Follow PEP 8 (checked with pylint)
- **Frontend**: Use ESLint & Prettier
- **Git**: Use conventional commits (feat:, fix:, docs:, etc.)

### Adding Features

**New export format?**
- Extend `backend/app/services/exporters.py`
- Add route to `backend/app/routers/export.py`
- Update frontend UI

**New API endpoint?**
- Add router module in `backend/app/routers/`
- Add tests in `backend/tests/`
- Document in code comments

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🔒 Environment & Secrets

See [Environment Configuration](#-secrets--environment-configuration) section above for setting up `.env` files and GitHub secrets.

---

**Version:** 2.1.0  
**Status:** ✅ Production Ready  
**Last Updated:** 2024

## 🔒 Secrets & Environment Configuration

### Local Development

1. **Create a `.env` file** from the template:
   ```bash
   cp .env.example .env
   ```

2. **Update values** in `.env` with your local development settings:
   ```bash
   DEBUG=True
   ENVIRONMENT=development
   DATABASE_URL=sqlite:///./telegram_export.db
   SECRET_KEY=your-development-secret-key
   ```

3. **Never commit `.env`** — it contains secrets. The `.env.example` file is provided as a reference.

4. **Add `.env` to `.gitignore`** (already configured in this repo).

### Environment Variables Reference

See `.env.example` for all available configuration options:

| Variable | Description | Example |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode (dev only) | `False` |
| `ENVIRONMENT` | deployment environment | `development`, `staging`, `production` |
| `DATABASE_URL` | Database connection string | `sqlite:///./telegram_export.db` |
| `SECRET_KEY` | Application secret key | Generate with `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `BACKEND_URL` | Backend API URL | `http://localhost:8000` |
| `FRONTEND_URL` | Frontend URL | `http://localhost:3000` |
| `STRIPE_API_KEY` | Stripe API key (optional) | `sk_test_...` |
| `SENTRY_DSN` | Sentry error tracking (optional) | `https://...@sentry.io/...` |

### GitHub Secrets for CI/CD

Secrets should be stored in GitHub repository settings for use in Actions workflows.

**To add a secret:**

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add secret name and value
4. Click **Add secret**

**Example: Using secrets in GitHub Actions**

```yaml
name: Deploy

on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install -r requirements.txt
      
      - name: Run with secrets
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          SECRET_KEY: ${{ secrets.SECRET_KEY }}
          STRIPE_API_KEY: ${{ secrets.STRIPE_API_KEY }}
          SENTRY_DSN: ${{ secrets.SENTRY_DSN }}
        run: |
          python app.py --init-db
          python app.py

      - name: Deploy to production
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
          BACKEND_URL: ${{ secrets.PROD_BACKEND_URL }}
        run: |
          # Your deployment script here
          bash ./scripts/deploy.sh
```

### Recommended Secrets to Configure

**Essential:**
- `SECRET_KEY` — Application secret (generate unique value per environment)
- `DATABASE_URL` — Production database connection

**Optional (if using these services):**
- `STRIPE_API_KEY` — Stripe payments
- `STRIPE_WEBHOOK_SECRET` — Stripe webhooks
- `SENTRY_DSN` — Error tracking
- `OPENAI_API_KEY` — AI features

### Security Best Practices

✅ **DO:**
- Generate strong, unique `SECRET_KEY` for production
- Rotate secrets regularly
- Use environment-specific values (dev ≠ staging ≠ prod)
- Store `.env` in secure location (never share)
- Use GitHub Secrets for CI/CD
- Mask sensitive data in logs

❌ **DON'T:**
- Commit `.env` or `.env.local` files
- Use weak or default secret keys
- Share secrets in chat, email, or code reviews
- Hardcode secrets in code
- Reuse secrets across environments
- Print secrets to stdout/logs

---

✨ **نسخة:** 2.0.0

## Backend processing

Processing is provided by backend.app.processor which exposes two simple
synchronous functions:

- process_export_from_file(file_path): process a JSON export file and return a
  structured result.
- process_export_from_payload(payload): process an in-memory export payload.

Functions are idempotent (they do not write files) and synchronous for the
MVP. For very large exports prefer streaming (ijson) or dispatching work to a
background worker (Celery/RQ) to avoid blocking the web worker.
