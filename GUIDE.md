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
│   ├── pages/            # Next.js pages/routes (index, dashboard, auth, pricing)
│   ├── components/       # UI components & Recharts widgets
│   ├── styles/           # Tailwind CSS configuration
│   └── package.json      # Node.js dependencies
│
├── backend/              # FastAPI app (Port 8000)
│   ├── app/
│   │   ├── main.py      # Entry point & CORS/Metrics Middleware
│   │   ├── auth.py      # JWT registration and login logic
│   │   ├── billing.py   # Stripe sessions & webhooks
│   │   ├── db.py        # SQLAlchemy SQLite engine
│   │   ├── models.py    # Database models (User schema)
│   │   ├── monitoring.py# Sentry & Prometheus integrations
│   │   ├── processor.py # Parse wrapper with usage checks
│   │   └── routers/     # API routers (web_ui uploads, exports)
│   ├── tests/           # Pytest unit tests
│   ├── requirements.txt # Python dependencies
│   └── Dockerfile       # Container setup
│
└── docker-compose.yml   # Local stack orchestration
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

### Quick Setup

**1. Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

**2. Configure Sentry (Optional but Recommended)**
```bash
# Get your Sentry DSN from https://sentry.io/
export SENTRY_DSN="https://key@sentry.io/project-id"
export ENV="production"  # or "development"

# Start backend
uvicorn app.main:app --reload
```

**3. Access Metrics**
```bash
# Health check
curl http://localhost:8000/health

# Prometheus metrics
curl http://localhost:8000/metrics
```

### Sentry Integration (Error Tracking)

**What it does:**
- Captures and tracks exceptions/errors
- Records performance metrics (10% sample rate in production)
- Groups errors for trend analysis
- Sends alerts for critical issues
- Integrates with FastAPI middleware automatically

**Setup Steps:**

1. **Create Sentry Account**
   - Go to https://sentry.io/signup/
   - Create organization and project
   - Select "Python → FastAPI" platform
   - Copy your DSN

2. **Add to Environment**
   ```bash
   # .env or deployment config
   SENTRY_DSN=https://key@sentry.io/project-id
   ENV=production
   APP_VERSION=1.0.0  # optional
   ```

3. **Verify Integration**
   ```bash
   # Test endpoint to trigger an error
   curl -X POST http://localhost:8000/api/process \
     -H "Content-Type: application/json" \
     -d '{"invalid": "data"}'
   
   # Check Sentry dashboard - error should appear within seconds
   ```

**Production Recommendations:**

| Setting | Development | Production |
|---------|-------------|-----------|
| **Traces Sample Rate** | 100% | 10% |
| **Profiles Sample Rate** | 0% | 10% |
| **Environment** | `development` | `production` |
| **Release** | Auto-detected | Set to semver (v1.2.3) |

**Alerting Rules (configure in Sentry):**

```
Alert when:
- Error rate > 5% in 5 minutes
- New issue appears
- Regression detected
- Performance threshold exceeded

Send to:
- Email
- Slack (integrate with #alerts channel)
- PagerDuty (for critical issues)
```

**Dashboard Recommendations:**

1. **Issues Dashboard**
   - Sort by "First Seen"
   - Filter by environment: `is:production`
   - Track regression issues

2. **Performance Dashboard**
   - Monitor transaction throughput
   - Check p95/p99 latencies
   - Track slowest endpoints

3. **Custom Alerts**
   - High error rate (> 5%)
   - Performance regression
   - New issue types
   - Critical exceptions (HTTP 500+)

### Prometheus Metrics

**Available Metrics:**

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `http_requests_total` | Counter | method, endpoint, status | Total HTTP requests by endpoint |
| `http_request_duration_seconds` | Histogram | method, endpoint, status | Request latency (0.01s to 10s buckets) |
| `http_requests_in_progress` | Gauge | - | Active requests (concurrent) |
| `exceptions_total` | Counter | exception_type | Total exceptions by type |
| `chat_processing_total` | Counter | status | Chat processing ops (success/failure) |
| `chat_processing_duration_seconds` | Histogram | status | Chat processing latency |

**Expose Metrics:**

```bash
# Prometheus format endpoint
curl http://localhost:8000/metrics

# Example output:
# TYPE http_requests_total counter
# http_requests_total{method="POST",endpoint="/api/process",status="200"} 42
# 
# TYPE http_request_duration_seconds histogram
# http_request_duration_seconds_bucket{method="GET",endpoint="/health",status="200",le="0.01"} 100
```

**Integration with Prometheus Server:**

1. **Install Prometheus**
   ```bash
   # macOS
   brew install prometheus
   
   # Linux/Docker
   docker run -d -p 9090:9090 prom/prometheus
   ```

2. **Configure Prometheus** (`prometheus.yml`)
   ```yaml
   global:
     scrape_interval: 15s
     evaluation_interval: 15s

   scrape_configs:
     - job_name: 'telegram-parser-backend'
       static_configs:
         - targets: ['localhost:8000']
       metrics_path: '/metrics'
   ```

3. **View Metrics Dashboard**
   - Open http://localhost:9090
   - Query examples:
     ```
     # Request rate (requests/sec)
     rate(http_requests_total[5m])
     
     # Error rate
     rate(http_requests_total{status=~"5.."}[5m])
     
     # P95 latency
     histogram_quantile(0.95, http_request_duration_seconds)
     
     # Active requests
     http_requests_in_progress
     
     # Chat processing success rate
     rate(chat_processing_total{status="success"}[5m])
     ```

**Integration with Grafana:**

1. **Install Grafana**
   ```bash
   docker run -d -p 3000:3000 grafana/grafana
   ```

2. **Add Prometheus Data Source**
   - Login: admin/admin
   - Configuration → Data Sources
   - Add Prometheus (http://localhost:9090)

3. **Create Dashboards**
   - Import template or create custom
   - Popular dashboards: FastAPI Monitoring (ID: 16589)

**Production Deployment:**

```docker
# docker-compose.yml
services:
  backend:
    image: telegram-export-backend
    environment:
      SENTRY_DSN: ${SENTRY_DSN}
      ENV: production
    ports:
      - "8000:8000"
  
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD}
```

**Key Metrics to Monitor:**

1. **System Health**
   - Error rate (HTTP 5xx)
   - Exception frequency
   - Active request count

2. **Performance**
   - Request latency (p50, p95, p99)
   - Chat processing duration
   - Throughput (requests/sec)

3. **Business Logic**
   - Chat processing success rate
   - Processing time trends
   - Export format distribution

**Alert Rules (Prometheus/Grafana):**

```yaml
# Alert when error rate > 5%
- alert: HighErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
  for: 5m
  annotations:
    summary: "Error rate > 5%"

# Alert when P95 latency > 1 second
- alert: HighLatency
  expr: histogram_quantile(0.95, http_request_duration_seconds) > 1
  for: 5m

# Alert when processing fails > 10% of time
- alert: ProcessingFailures
  expr: rate(chat_processing_total{status="failure"}[5m]) > 0.10
  for: 5m
```

### Environment Variables

```bash
# Sentry
SENTRY_DSN=https://key@sentry.io/project-id
ENV=production  # development, staging, production
APP_VERSION=1.0.0

# Optional Sentry settings
SENTRY_TRACES_SAMPLE_RATE=0.1  # 10% for production
SENTRY_PROFILES_SAMPLE_RATE=0.1
```

### Monitoring Checklist

- [ ] Sentry project created and DSN configured
- [ ] `/metrics` endpoint accessible
- [ ] Prometheus scraping metrics successfully
- [ ] Grafana dashboards created
- [ ] Alert rules configured (error rate, latency, failures)
- [ ] Team notified of Sentry/Grafana URLs
- [ ] Documentation updated with monitoring links
- [ ] Log aggregation configured (optional)
- [ ] On-call rotation setup
- [ ] Incident response playbook created

---

## 🔧 Manual Monitoring (Without External Services)

If you can't use Sentry/Prometheus externally:

**Simple Logging:**
```python
# backend/app/monitoring.py
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In your code:
logger.info("Processing export", extra={"chat_id": 123, "msg_count": 500})
logger.error("Processing failed", exc_info=True)
```

**Local Metrics File:**
```python
# Write metrics to disk for analysis
with open('metrics.log', 'a') as f:
    f.write(f"{time.time()},{method},{endpoint},{status},{duration}\n")
```

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
**Last Updated:** June 2026
