# 🚀 Telegram Export Parser - Developer & Deployment Guide

## 📖 Overview

This guide covers:
- **Developer Workflow** - How to work on this project locally
- **Architecture & Services** - Understanding the multi-service setup
- **Deployment** - How to deploy to production
- **CI/CD** - GitHub Actions automation
- **Troubleshooting** - Common issues & solutions

---

## 👨‍💻 Developer Workflow

### 1. Local Development Environment

#### Prerequisites
- Git
- Docker & Docker Compose
- OR: Node.js 18+, Python 3.11+

#### Initial Setup

```bash
# Clone repository
git clone <repo-url>
cd Telegram\ Export\ Parser

# Create feature branch
git checkout -b feature/your-feature

# Option A: Using Docker (recommended)
docker-compose up --build

# Option B: Manual setup (see README.md)
```

#### Project Structure Overview

```
root/
├── frontend/              # Next.js/TypeScript app (Port 3000)
│   ├── pages/            # Next.js pages/routes
│   ├── components/       # React components
│   ├── styles/           # Tailwind CSS
│   ├── package.json
│   └── tsconfig.json
│
├── backend/              # FastAPI app (Port 8000)
│   ├── app/
│   │   ├── main.py      # Entry point
│   │   ├── routers/     # API endpoints
│   │   ├── models/      # Pydantic models
│   │   └── services/    # Business logic
│   ├── tests/           # pytest test files
│   ├── requirements.txt
│   └── Dockerfile
│
└── docker-compose.yml   # Local dev orchestration
```

### 2. Making Changes

#### Backend Development

```bash
# 1. Start backend in development mode
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# 2. Make changes to app/
# Changes automatically reload thanks to --reload flag

# 3. Test your changes
pytest

# 4. Check code style
pylint app/
black --check app/

# 5. Format code
black app/
```

#### Frontend Development

```bash
# 1. Start frontend development server
cd frontend
npm install
npm run dev

# 2. Make changes to pages/ or components/
# Changes automatically reload (hot reload)

# 3. Test your changes
npm run test

# 4. Lint code
npm run lint

# 5. Format code
npm run format
```

### 3. Testing

```bash
# Backend: Run all tests
cd backend
pytest

# Backend: Run specific test
pytest tests/test_export.py -v

# Backend: With coverage
pytest --cov=app tests/

# Frontend: Run all tests
cd frontend
npm run test

# Frontend: Watch mode
npm run test -- --watch
```

### 4. Code Review & Commits

**Conventional Commit Format:**

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Code style (formatting, semicolons, etc.)
- `refactor:` - Code refactoring
- `perf:` - Performance improvement
- `test:` - Test addition/modification
- `chore:` - Build, deps, tooling

**Examples:**
```bash
git commit -m "feat(export): add XLSX multi-sheet support"
git commit -m "fix(api): handle empty chat messages correctly"
git commit -m "docs(readme): update deployment instructions"
```

### 5. Creating Pull Requests

```bash
# Push your feature branch
git push origin feature/your-feature

# Go to GitHub and create PR
# → Set base branch: main
# → Provide clear description
# → Link related issues
# → Request reviewers
```

**PR Description Template:**

```markdown
## Description
Brief explanation of changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Breaking change

## Testing
- [ ] Tested locally
- [ ] All tests pass
- [ ] Added new tests

## Checklist
- [ ] Code follows style guide
- [ ] No new warnings generated
- [ ] Documentation updated
```

---

## 🚀 Deployment

### Overview of Deployment Strategy

| Component | Service | Environment | URL |
|-----------|---------|-------------|-----|
| **Frontend** | Vercel | Production | `https://telegram-parser.vercel.app` |
| **Backend** | Google Cloud Run | Production | `https://api.telegram-parser.com` |
| **Database** | Cloud SQL/PostgreSQL | Production | Managed by GCP |
| **Secrets** | GitHub Secrets | CI/CD | Used by Actions |

### Frontend Deployment (Vercel)

#### Setup (One-time)

1. **Connect GitHub to Vercel:**
   - Go to https://vercel.com
   - Click "Import Project"
   - Select GitHub repository
   - Authorize Vercel

2. **Configure Environment:**
   ```bash
   # In Vercel dashboard, add Environment Variables
   NEXT_PUBLIC_API_URL=https://api.telegram-parser.com
   NEXT_PUBLIC_APP_ENV=production
   ```

3. **Configure Build:**
   - Framework: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Install Command: `npm install`

#### Deploying

**Automatic (Recommended):**
```bash
# Push to main branch - Vercel automatically deploys
git push origin main
```

**Manual:**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from project root
vercel --prod
```

**Preview Deployments:**
```bash
# Every PR automatically gets a preview URL
# Posted as comment on PR
```

### Backend Deployment (Google Cloud Run / AWS ECS)

#### Prerequisites

- Google Cloud project OR AWS account
- Docker installed locally
- `gcloud` CLI installed (for GCP)

#### Option A: Google Cloud Run (Recommended)

```bash
# 1. Configure project
gcloud config set project PROJECT_ID
gcloud auth configure-docker

# 2. Build & push image
docker build -f backend/Dockerfile -t gcr.io/PROJECT_ID/telegram-export-backend backend
docker push gcr.io/PROJECT_ID/telegram-export-backend

# 3. Deploy to Cloud Run
gcloud run deploy telegram-export-backend \
  --image gcr.io/PROJECT_ID/telegram-export-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ENVIRONMENT=production

# 4. Get service URL
gcloud run services describe telegram-export-backend \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

**Auto-deploy with Cloud Build:**

```bash
# Create cloudbuild.yaml in root
# Set up trigger in Cloud Build console
# Triggers on push to main branch
```

#### Option B: AWS ECS

```bash
# 1. Create ECR repository
aws ecr create-repository --repository-name telegram-export-backend

# 2. Build & push image
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

docker build -f backend/Dockerfile -t telegram-export-backend backend
docker tag telegram-export-backend:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/telegram-export-backend:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/telegram-export-backend:latest

# 3. Deploy using ECS console or CLI
# Configure task definition, service, load balancer
```

#### Environment Variables

```bash
# Set in Cloud Run/ECS environment
ENVIRONMENT=production
DATABASE_URL=postgresql://user:pass@cloudsql-ip/dbname
SECRET_KEY=<generate-with-secrets-manager>
SENTRY_DSN=https://key@sentry.io/project
CORS_ORIGINS=https://telegram-parser.vercel.app
LOG_LEVEL=info
```

---

## 🔄 CI/CD with GitHub Actions

### Setup

1. **Create `.github/workflows/` directory**

2. **Create workflow files:**

#### `ci.yml` - Tests on every commit

```yaml
name: CI

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: |
          cd backend
          pip install -r requirements.txt
          pytest

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - run: |
          cd frontend
          npm install
          npm run lint
          npm run test
```

#### `deploy.yml` - Deploy on merge to main

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: google-github-actions/setup-gcloud@v1
        with:
          service_account_key: ${{ secrets.GCP_KEY }}
          project_id: ${{ secrets.GCP_PROJECT_ID }}
          export_default_credentials: true
      
      - run: |
          gcloud auth configure-docker
          docker build -f backend/Dockerfile -t gcr.io/${{ secrets.GCP_PROJECT_ID }}/telegram-export-backend backend
          docker push gcr.io/${{ secrets.GCP_PROJECT_ID }}/telegram-export-backend
          gcloud run deploy telegram-export-backend \
            --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/telegram-export-backend \
            --region us-central1 \
            --set-env-vars DATABASE_URL=${{ secrets.DATABASE_URL }}

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: vercel/action@main
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          production: true
```

### GitHub Secrets to Configure

In **Settings → Secrets and variables → Actions**, add:

```
GCP_KEY                    # Service account key (JSON)
GCP_PROJECT_ID            # Google Cloud project ID
DATABASE_URL              # Production database URL
SECRET_KEY                # Application secret key
VERCEL_TOKEN              # Vercel API token
VERCEL_ORG_ID             # Vercel org ID
VERCEL_PROJECT_ID         # Vercel project ID
SENTRY_DSN                # Sentry error tracking URL
```

---

## 🐛 Troubleshooting

### Common Issues

#### Issue: "Backend connection refused"
```bash
# Check if backend is running
curl http://localhost:8000/docs

# If not running, restart it
cd backend
uvicorn app.main:app --reload --port 8000
```

#### Issue: "Port already in use"
```bash
# Kill process on port
# macOS/Linux:
lsof -i :8000
kill -9 <PID>

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

#### Issue: "Module not found" (Python)
```bash
# Ensure virtual environment activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### Issue: "npm dependencies outdated"
```bash
cd frontend
npm install  # Update to latest compatible versions
npm ci       # Use exact versions from package-lock.json
```

#### Issue: "Docker build fails"
```bash
# Clear cache and rebuild
docker-compose down
docker system prune -a
docker-compose up --build --no-cache
```

### Debug Mode

**Backend:**
```python
# Add to app/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Frontend:**
```javascript
// Add to next.config.js
module.exports = {
  env: {
    DEBUG: true
  }
}
```

---

## 📊 Monitoring & Observability

### Sentry (Error Tracking)

```python
# In backend/app/main.py
import sentry_sdk
sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    environment=os.getenv('ENVIRONMENT', 'development'),
    traces_sample_rate=1.0
)
```

### Logging

```python
# Centralized logging in backend
import logging
logger = logging.getLogger(__name__)

logger.info("Export started", extra={"chat_id": chat_id})
logger.error("Export failed", exc_info=True)
```

### Performance Monitoring

- **Frontend**: Use Next.js Analytics
- **Backend**: Use Cloud Run metrics dashboard
- **Database**: Monitor with Cloud SQL/RDS console

---

## 📚 Additional Resources

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Google Cloud Run](https://cloud.google.com/run/docs)
- [AWS ECS](https://docs.aws.amazon.com/ecs/)
- [GitHub Actions](https://docs.github.com/en/actions)

---

**Version:** 2.1.0  
**Status:** ✅ Production Ready  
**Last Updated:** 2024
