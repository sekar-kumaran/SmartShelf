# VIF SmartShelf — Deployment Plan

**Version:** 0.1.0  
**Date:** 2026-10-17  
**Status:** Proposed

---

## 1. Deployment Phases

### Phase A — Local Development

**Goal:** All services run on a developer's machine via Docker Compose.

**Services:**
| Service | Technology | Port |
|---|---|---|
| Frontend | Next.js (dev server) | 3000 |
| Inference API | FastAPI + Uvicorn | 8000 |
| PostgreSQL | PostgreSQL 16 | 5432 |

**Commands:**
```bash
# Start all services
make dev

# Or manually:
docker compose up -d db
cd apps/services/inference-api && uvicorn app.main:app --reload --port 8000
cd apps/web && npm run dev
```

**Prerequisites:**
- Docker Desktop (or Podman) installed.
- Node.js 20+ installed.
- Python 3.11+ installed.
- `.env` file created from `.env.example`.
- Model artifact downloaded and placed at path in `.env`.

**Note:** The API will start in `model-not-ready` state if `best.pt` is not present. `/health/ready` will return 503. The frontend will show a model unavailable warning. Demo mode will still work.

---

### Phase B — ML Experimentation (Google Colab)

**Goal:** Train and validate the model using Colab GPU.

**Process:**
1. Open notebooks in Google Colab (upload from `ml/notebooks/`).
2. Mount Google Drive for persistent storage.
3. Run notebooks 00 → 09 in sequence.
4. Export final model artifact from Notebook 09.
5. Upload artifact to Hugging Face Hub or Cloudflare R2.
6. Record checksum and update `artifacts/models/smartshelf/SHA256SUMS.txt`.

**Constraints:**
- Colab free tier: T4 GPU, session limit ~12h. Use Pro for longer sessions.
- Large checkpoints must be saved to Drive, not committed to Git.
- Only the final `best.pt` and metadata are published; intermediate checkpoints stay in Drive.

---

### Phase C — Frontend Hosting (Vercel)

**Platform:** Vercel  
**Trigger:** Push to `main` branch  

**Configuration:**
```
Root directory: apps/web
Build command: npm run build
Output: .next (Next.js)
Node version: 20.x
```

**Environment variables (Vercel dashboard):**
```
INFERENCE_API_URL=https://api.smartshelf.yourdomain.com
NEXT_PUBLIC_DEMO_MODE=false
```

**Important:** Never set `NEXT_PUBLIC_INFERENCE_API_URL` — the API URL must stay server-side to prevent CORS bypass and URL exposure.

**Preview deployments:** Enabled for all PRs. Preview URLs use demo mode by default.

---

### Phase D — Backend Hosting (Oracle Cloud VM)

**Platform:** Oracle Cloud Infrastructure (OCI) — Free Tier ARM VM (Ampere A1)

**Specification assessment:**
| Factor | Free Tier Value | Requirement |
|---|---|---|
| vCPUs | 4 (ARM Ampere A1) | 2+ needed for API + Nginx |
| RAM | 24 GB | YOLOv8n: ~300 MB loaded; 4 GB+ comfortable |
| Storage | 200 GB block | 20 GB sufficient for app + model |
| Network | 10 TB outbound/month | Sufficient for early users |
| Cost | Free (subject to Oracle policy) | Target: $0 initially |
| GPU | None | CPU inference only |

**⚠️ Important Caveats:**
- Oracle Free Tier availability varies by region. Not guaranteed.
- Arm64 architecture — Docker images must be built for `linux/arm64`.
- Oracle can reclaim unused instances. Monitor activity.
- Free Tier terms may change. Budget for paid fallback ($20–40/month for 2 vCPU VM).

**Deployment stack on VM:**
```
VM (Ubuntu 22.04 LTS, ARM64)
├── Nginx (reverse proxy, TLS termination)
│   └── /etc/nginx/sites-available/smartshelf
├── Docker (container runtime)
│   ├── Container: smartshelf-api (FastAPI + Uvicorn)
│   └── Container: smartshelf-db (PostgreSQL — if not using Neon)
├── Certbot (Let's Encrypt TLS)
└── UFW (firewall — allow 80, 443 only)
```

**Docker deployment commands:**
```bash
# On the VM, first-time setup
docker pull ghcr.io/your-org/smartshelf-api:v0.1.0
docker run -d \
  --name smartshelf-api \
  --restart unless-stopped \
  -p 8000:8000 \
  --env-file /etc/smartshelf/.env \
  -v /opt/smartshelf/models:/app/models:ro \
  ghcr.io/your-org/smartshelf-api:v0.1.0
```

**CPU inference latency benchmark target:**
- YOLOv8n on 640×640: expected ~50–150 ms on 4× Ampere A1 cores.
- Acceptable for single-image upload use case.
- Benchmark must be run before committing to this platform.

**Alternative backend platforms:**

| Platform | Cost | GPU | Notes |
|---|---|---|---|
| Oracle Cloud Free Tier | $0 | None | Free but conditional |
| Railway.app | $5–20/month | None | Simple Docker deploy |
| Render.com | $7–25/month | None | Good developer UX |
| Fly.io | $0–15/month | None | Global CDN for API |
| AWS Lightsail | $3.50–20/month | None | Reliable, not free |
| Google Cloud Run | Pay-per-request | None | Cold starts; OK for low volume |
| Modal.com | Pay-per-use | YES (CUDA) | For future GPU serving |

---

### Phase E — Database Hosting (Neon)

**Platform:** Neon — managed serverless PostgreSQL

**Assessment:**

| Factor | Neon Free Tier |
|---|---|
| Storage | 512 MB (sufficient for MVP) |
| Compute | 0.25 vCPU, auto-suspend after 5 min idle |
| Connections | 100 max (use PgBouncer for pooling) |
| Region | Choose closest to backend VM |
| Backups | Automatic branching / point-in-time restore |
| Cost | Free (current) — monitor for policy changes |

**Connection string format:**
```
DATABASE_URL=postgresql+asyncpg://user:pass@ep-xxx.region.aws.neon.tech/smartshelf?sslmode=require
```

**Migration command:**
```bash
alembic upgrade head
```

**⚠️ Neon auto-suspends after 5 min idle.** First connection after idle takes ~1–2 seconds. This is acceptable for MVP. For production, keep-alive pings or a paid plan may be needed.

---

### Phase F — Model Storage (Hugging Face Hub)

**Platform:** Hugging Face Hub (free public or private repos)

**Model repo structure:**
```
your-org/smartshelf-models/
├── v0.1.0/
│   ├── best.pt              # Main model weights
│   ├── model_metadata.json  # Version, classes, config
│   ├── class_mapping.json   # Class ID to name mapping
│   ├── evaluation_summary.json
│   ├── model_card.md
│   └── SHA256SUMS.txt
└── README.md
```

**API server model loading:**
```python
# At startup, the API fetches the specific version
from huggingface_hub import hf_hub_download

model_path = hf_hub_download(
    repo_id="your-org/smartshelf-models",
    filename="v0.1.0/best.pt",
    cache_dir="/app/models"
)
```

**Important:** The API downloads and caches the model on startup. It does NOT re-download on every request. Checksum is verified after download.

**Alternative: Cloudflare R2** — use if model must be private, or if HF Hub access is slow from the VM region.

---

### Phase G — GPU Inference (Future)

**Decision: Do NOT provision GPU in MVP.**

GPU serving is evaluated only if:
1. CPU inference benchmarks show p95 latency > 2 seconds under expected concurrent load.
2. User demand justifies GPU cost.

**If needed, evaluate:**
| Platform | GPU | Cost | Notes |
|---|---|---|---|
| Modal.com | T4/A10G | ~$0.10/hr | Pay per use, cold starts |
| Replicate | Various | Pay per run | Easy deployment |
| Runpod | A100/H100 | $0.30–2.50/hr | Cheap if persistent |
| Google Cloud | T4 | $0.35/hr | Stable, reliable |
| AWS SageMaker | Various | Complex pricing | For scale |

---

### Phase H — CI/CD (GitHub Actions)

**Workflow files:**

```yaml
# .github/workflows/frontend.yml
on: [push, pull_request]
jobs:
  lint-typecheck:
    runs-on: ubuntu-latest
    steps:
      - npm ci
      - npm run type-check
      - npm run lint
  test:
    steps:
      - npm run test
  build:
    steps:
      - npm run build

# .github/workflows/backend.yml
on: [push, pull_request]
jobs:
  lint:
    steps:
      - pip install ruff mypy
      - ruff check .
      - mypy .
  test:
    steps:
      - pytest tests/

# .github/workflows/docker.yml
on:
  push:
    branches: [main]
    tags: ['v*']
jobs:
  build-push:
    steps:
      - docker buildx build --platform linux/arm64 ...
      - docker push ghcr.io/...
```

**Rules:**
- Never print secrets in CI logs.
- Deploy to production only after all checks pass.
- Integration tests use a test database, not production.

---

### Phase I — Domain and Production Readiness

**Required before production claim:**

- [ ] Custom domain configured (e.g., `smartshelf.vif.in`)
- [ ] DNS records pointing to Vercel (frontend) and VM (API)
- [ ] HTTPS enabled on API (Let's Encrypt via Certbot)
- [ ] CORS configured to allow only the production frontend domain
- [ ] Upload size limit set in Nginx (`client_max_body_size 15m;`)
- [ ] Rate limiting configured (SlowAPI: 10 req/min per IP)
- [ ] Privacy policy published (noting image retention period)
- [ ] Terms of use published
- [ ] Dataset attribution on Settings page and model card
- [ ] Incident response procedure documented
- [ ] Backup and recovery procedure tested
- [ ] Monitoring alerts configured (uptime + error rate)

---

## 2. Environment Variables Reference

```bash
# .env.example (commit this — no secrets)

# Application
APP_ENV=development  # development | production
LOG_LEVEL=INFO

# Model
MODEL_ARTIFACT_PATH=/app/models/smartshelf/best.pt
MODEL_VERSION=v0.1.0
MODEL_SHA256=<fill-after-training>
HF_MODEL_REPO=your-org/smartshelf-models

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/smartshelf

# API settings
MAX_UPLOAD_SIZE_MB=10
INFERENCE_CONFIDENCE_THRESHOLD=0.25
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# Frontend (apps/web/.env.local)
INFERENCE_API_URL=http://localhost:8000
NEXT_PUBLIC_DEMO_MODE=true
```

---

## 3. Health Check Endpoints

| Endpoint | Expected Response | Failure Behaviour |
|---|---|---|
| `GET /health/live` | 200 always (process alive) | Container restart if 5 consecutive failures |
| `GET /health/ready` | 200 if model loaded, 503 otherwise | Excluded from load balancer if 503 |

---

## 4. Deployment Checklist (Pre-Release)

- [ ] Model artifact checksum verified on server.
- [ ] `/health/ready` returns 200.
- [ ] POST a real test image, verify structured JSON response.
- [ ] Frontend connects to API (network tab shows 200 from API).
- [ ] Demo mode toggle visible and working.
- [ ] Analysis history shows entries after uploads.
- [ ] HTTPS certificate valid (check with `openssl s_client`).
- [ ] Firewall blocks direct DB port (5432) from public internet.
- [ ] Logs are writing correctly.
- [ ] Monitoring alert fired a test notification.

---

*Deployment plan version 0.1.0 — updated as infrastructure decisions are confirmed.*
