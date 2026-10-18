# VIF SmartShelf — Architecture

**Version:** 0.1.0  
**Date:** 2026-10-17  
**Status:** Proposed — Phase 0

---

## 1. Architecture Overview

VIF SmartShelf is a **modular monorepo** containing four distinct layers:

```
vif-smartshelf/
├── apps/
│   ├── web/                     # Next.js 14 frontend
│   └── services/
│       └── inference-api/       # FastAPI inference service
├── ml/                          # ML pipeline (notebooks + scripts)
│   ├── notebooks/               # Google Colab notebooks (00-10)
│   ├── configs/                 # Training configs (YAML)
│   └── src/                     # Python ML library
├── artifacts/
│   └── models/smartshelf/       # Released model artifacts
├── infra/
│   ├── docker/                  # Dockerfiles
│   └── deployment/              # Deployment configs
├── docs/                        # All documentation
└── .github/workflows/           # CI/CD
```

---

## 2. System Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                        USER BROWSER                     │
│                                                         │
│   ┌─────────────────────────────────────────────────┐   │
│   │             Next.js 14 Frontend                 │   │
│   │   (Vercel — CDN-served, TypeScript + Tailwind)  │   │
│   │                                                 │   │
│   │  Landing │ Dashboard │ Analysis │ History        │   │
│   │  Detection Review │ Occupancy │ Reports          │   │
│   └──────────────────┬──────────────────────────────┘   │
└─────────────────────-│──────────────────────────────────┘
                       │ HTTPS REST API calls
                       │ (multipart/form-data for images)
┌──────────────────────▼──────────────────────────────────┐
│           FastAPI Inference Service (Python)             │
│              (Docker · Oracle Cloud VM)                  │
│                                                         │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ API Routes │  │ Image Valid. │  │ Model Loader    │  │
│  │ /health/*  │  │ + Preprocess │  │ (loaded once at │  │
│  │ /api/v1/*  │  │              │  │  startup)       │  │
│  └────────────┘  └──────────────┘  └────────┬────────┘  │
│                                             │            │
│  ┌──────────────────────────────────────────▼────────┐  │
│  │           Ultralytics YOLO Inference               │  │
│  │         (CPU inference · best.pt artifact)         │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌────────────────────────────────────────────────────┐  │
│  │              Analysis Repository                   │  │
│  │          (PostgreSQL via Alembic ORM)               │  │
│  └────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                       │
         ┌─────────────▼──────────────┐
         │  Model Artifact Storage    │
         │  (Hugging Face Hub / R2)   │
         │  best.pt + metadata.json   │
         └────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              Google Colab (Training Only)                │
│                                                         │
│  Notebooks 00-10 → train → export → publish artifact    │
│  NEVER used as production inference server              │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Component Descriptions

### 3.1 Next.js Frontend (`apps/web/`)

| Aspect | Decision |
|---|---|
| Framework | Next.js 14 (App Router) |
| Language | TypeScript (strict) |
| Styling | Tailwind CSS |
| API client | Fetch + React Query |
| State | Zustand (UI state) |
| Forms | React Hook Form + Zod |
| Image overlay | HTML Canvas (bounding boxes) |
| Auth | None in MVP (single-user / open) |
| Deployment | Vercel |

**Key architectural decisions:**
- All API calls go through a server-side environment variable (`INFERENCE_API_URL`), never exposed in the frontend bundle.
- Demo mode is toggled via a client-side flag, never via server state.
- Bounding box rendering uses a Canvas element overlaid on the uploaded image.

### 3.2 FastAPI Inference Service (`apps/services/inference-api/`)

| Aspect | Decision |
|---|---|
| Framework | FastAPI 0.115+ |
| Python | 3.11 |
| ASGI server | Uvicorn (behind Nginx reverse proxy) |
| ML library | Ultralytics 8.x |
| Image processing | Pillow + OpenCV |
| ORM | SQLAlchemy 2.x + Alembic |
| Database | PostgreSQL 16 |
| Validation | Pydantic v2 |
| Deployment | Docker container |

**Key architectural decisions:**
- Model is loaded **once at startup** (`lifespan` event) and reused for all requests.
- If model file is missing or checksum fails, service starts in `model-not-ready` state and `/health/ready` returns 503.
- Image uploads are streamed to a temporary file, validated, processed, then cleaned up.
- No model training occurs during any user request.
- Database stores analysis metadata and detection summaries, not raw image blobs.

**Directory layout:**
```
inference-api/
├── app/
│   ├── main.py           # FastAPI app + lifespan
│   ├── api/
│   │   ├── health.py     # /health/live, /health/ready
│   │   ├── model.py      # /api/v1/model/info
│   │   ├── detections.py # /api/v1/detections
│   │   └── analyses.py   # /api/v1/analyses/*
│   ├── core/
│   │   ├── config.py     # Settings (pydantic-settings)
│   │   ├── model_loader.py
│   │   └── inference.py  # Preprocessing + postprocessing
│   ├── schemas/
│   │   ├── detection.py  # Request/response schemas
│   │   └── analysis.py
│   ├── models/
│   │   └── analysis.py   # SQLAlchemy ORM models
│   ├── repositories/
│   │   └── analysis_repo.py
│   └── security/
│       ├── upload.py     # File validation
│       └── rate_limit.py
├── tests/
├── alembic/
├── Dockerfile
└── pyproject.toml
```

### 3.3 ML Pipeline (`ml/`)

All ML work runs in Google Colab notebooks. The local `ml/` directory contains:
- Notebook source files (synced from Colab via Drive or manual download).
- Training config YAML files.
- Python scripts for data utilities (usable locally for validation).
- No large binary files committed.

### 3.4 Artifacts (`artifacts/`)

Released model artifacts are stored here as a **reference only** — the actual files live in Hugging Face Hub or Cloudflare R2. The local directory contains:
- `models/smartshelf/model_metadata.json` — version, classes, evaluation metrics.
- `models/smartshelf/class_mapping.json` — class ID to class name mapping.
- `models/smartshelf/SHA256SUMS.txt` — checksums for verification.
- **NOT committed:** `best.pt` (too large for Git).

---

## 4. Data Flow — Image Analysis Request

```
1. User drags image to frontend upload zone
2. Frontend validates file type and size (client-side)
3. POST /api/v1/detections (multipart/form-data)
4. FastAPI validates file type, size, dimensions (server-side)
5. Image decoded to PIL/numpy array
6. Resized to model input size (640×640) with letterboxing
7. YOLO model infers (returns boxes, scores, class IDs)
8. Results post-processed:
   - NMS applied (handled by YOLO internally)
   - Coordinates de-scaled back to original image space
   - Class IDs mapped to class names via class_mapping.json
   - Confidence filtered (threshold configurable, default 0.25)
9. Analysis saved to PostgreSQL (metadata + detections)
10. Temporary image file deleted
11. Response JSON returned to frontend
12. Frontend renders bounding boxes on Canvas overlay
```

---

## 5. API Contract Summary

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/health/live` | None | Liveness — always 200 if process is up |
| GET | `/health/ready` | None | Readiness — 503 if model not loaded |
| GET | `/api/v1/model/info` | None | Model version, classes, evaluation summary |
| POST | `/api/v1/detections` | None (MVP) | Run detection on uploaded image |
| POST | `/api/v1/shelf-analysis` | None (MVP) | Run full shelf analysis |
| GET | `/api/v1/analyses` | None (MVP) | Paginated analysis history |
| GET | `/api/v1/analyses/{id}` | None (MVP) | Single analysis result |

All responses use `Content-Type: application/json`.  
All error responses use RFC 7807 Problem Detail format.

---

## 6. Database Schema (Proposed)

```sql
-- Model versions registry
CREATE TABLE model_versions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version     TEXT NOT NULL UNIQUE,
    architecture TEXT NOT NULL,
    class_count INTEGER NOT NULL,
    map50       REAL,
    map50_95    REAL,
    artifact_url TEXT,
    artifact_sha256 TEXT,
    released_at TIMESTAMPTZ NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Analysis records
CREATE TABLE analyses (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_version_id UUID REFERENCES model_versions(id),
    image_filename  TEXT,
    image_width     INTEGER NOT NULL,
    image_height    INTEGER NOT NULL,
    image_format    TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'pending',
    total_detections INTEGER,
    processing_time_ms INTEGER,
    warnings        JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Individual detections
CREATE TABLE analysis_detections (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_id UUID NOT NULL REFERENCES analyses(id) ON DELETE CASCADE,
    class_id    INTEGER NOT NULL,
    class_name  TEXT NOT NULL,
    confidence  REAL NOT NULL,
    x_min       INTEGER NOT NULL,
    y_min       INTEGER NOT NULL,
    x_max       INTEGER NOT NULL,
    y_max       INTEGER NOT NULL
);

-- Per-analysis class counts
CREATE TABLE analysis_class_counts (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_id UUID NOT NULL REFERENCES analyses(id) ON DELETE CASCADE,
    class_name  TEXT NOT NULL,
    count       INTEGER NOT NULL
);
```

---

## 7. Security Architecture

| Concern | Mitigation |
|---|---|
| Arbitrary file upload | Server-side type validation (magic bytes, not extension), size limit |
| Path traversal | Secure temp filename generation (uuid), no user-controlled paths |
| Large image DoS | Dimension limit + file size limit |
| Secret leakage | All secrets in env vars, never in source code |
| CORS | Explicit allow-list, no wildcard in production |
| SQL injection | SQLAlchemy ORM parameterisation |
| Rate limiting | SlowAPI (token bucket per IP) |
| HTTPS | Nginx TLS termination (Let's Encrypt) |

---

## 8. Deployment Architecture

See `docs/DEPLOYMENT_PLAN.md` for full detail.

**Summary:**
- Frontend: Vercel (auto-deploy on main branch push)
- Backend: Oracle Cloud VM (Dockerised, Nginx reverse proxy)
- Database: Neon (managed PostgreSQL, free tier)
- Model storage: Hugging Face Hub (versioned, checksum-verified)
- CI/CD: GitHub Actions

---

## 9. Architecture Decision Records

### ADR-001: Use FastAPI (not Flask or Django)
**Decision:** FastAPI  
**Reason:** Native Pydantic v2 validation, async support, auto-generated OpenAPI docs, excellent performance for I/O-bound inference workloads.  
**Date:** 2026-10-17

### ADR-002: Load model once at startup
**Decision:** Use FastAPI `lifespan` to load YOLO model before accepting requests.  
**Reason:** Model loading (disk I/O + weight allocation) takes several seconds. Loading per-request would make the service unusable.  
**Date:** 2026-10-17

### ADR-003: No model training during inference requests
**Decision:** The inference service only loads pre-trained artifacts. Training runs only in Colab notebooks.  
**Reason:** Training on user hardware or during user requests is unreliable, slow, and creates serious security risks.  
**Date:** 2026-10-17

### ADR-004: Demo mode as client-side toggle
**Decision:** Demo mode is a frontend-only state. The API is not involved.  
**Reason:** Demo mode must work without API connectivity (for presentations, demos without backend).  
**Date:** 2026-10-17

### ADR-005: Bounding boxes as pixel-absolute xyxy
**Decision:** All bounding boxes use pixel-absolute `x_min, y_min, x_max, y_max` in original image space.  
**Reason:** Unambiguous, widely understood, easy to render on Canvas.  
**Date:** 2026-10-17

### ADR-006: Defer background job queue
**Decision:** No Celery/Redis in MVP. Synchronous inference only.  
**Reason:** Must first benchmark actual CPU inference latency. Queue adds significant complexity without confirmed need.  
**Date:** 2026-10-17

---

*Architecture document v0.1.0 — reviewed and updated per phase.*
