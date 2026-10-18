# VIF SmartShelf — Risks and Decisions

**Version:** 0.1.0  
**Date:** 2026-10-17  
**Format:** Risk Register + Architecture Decision Records (ADRs)

---

## Part 1: Risk Register

### Risk Scoring
- **Probability:** 1 (Low) · 2 (Medium) · 3 (High)
- **Impact:** 1 (Low) · 2 (Medium) · 3 (High)
- **Score:** Probability × Impact

---

### R-01 — Grocer-Help dataset files are restricted

| Field | Value |
|---|---|
| Category | Dataset / Blocker |
| Probability | 3 (confirmed restricted) |
| Impact | 3 (no training data) |
| Score | 9 (Critical) |
| Status | OPEN |
| Affected phases | 1, 2, 3 |

**Evidence:** Zenodo record page states "The record is publicly accessible, but files are restricted. Log in to check if you have access."

**Impact:** Cannot download training data, cannot run any ML notebooks, cannot train any model. The entire ML pipeline is blocked.

**Proposed mitigations:**
1. **(Immediate)** Create a Zenodo account and attempt download. Some datasets are restricted to logged-in users only (no further approval needed).
2. **(If needed)** Contact Mayank Sah and Jimson Mathew at IIT Patna requesting dataset access.
3. **(Fallback)** If access is denied, pivot to Roboflow Indian Grocery dataset as primary (after license verification), supplemented by VIF custom data collection.
4. **(Parallel)** Begin VIF custom data collection planning regardless, to reduce dependency on external datasets.

**Acceptance criteria for closure:** Dataset files downloaded, file count verified, annotation format confirmed.

---

### R-02 — Roboflow dataset access denied (HTTP 403)

| Field | Value |
|---|---|
| Category | Dataset |
| Probability | 2 |
| Impact | 2 |
| Score | 4 (Medium) |
| Status | OPEN |
| Affected phases | 1, 2 |

**Evidence:** HTTP 403 returned when attempting to load the Roboflow Universe page without authentication.

**Impact:** Cannot verify dataset contents, class names, image quality, or license without login. Unknown whether dataset is suitable or commercially licensed.

**Proposed mitigations:**
1. Create a free Roboflow account and inspect the dataset.
2. If license does not permit commercial use, exclude entirely.
3. If class labels are incompatible with Grocer-Help, use only as supplementary data for classes not covered by Grocer-Help.

**Acceptance criteria for closure:** Dataset inspected, class names documented, license confirmed.

---

### R-03 — SKU-110K commercial licensing unconfirmed

| Field | Value |
|---|---|
| Category | Legal |
| Probability | 3 (assumed restricted) |
| Impact | 3 (legal risk) |
| Score | 9 (Critical) |
| Status | MITIGATED (excluded) |

**Evidence:** CVPR academic paper dataset. No explicit commercial license found. Standard academic dataset terms restrict commercial use.

**Mitigation applied:** SKU-110K excluded from all training until commercial license is explicitly confirmed in writing. Decision recorded in `DATASET_AND_LICENSE_AUDIT.md`.

---

### R-04 — No trained model artifact exists at project start

| Field | Value |
|---|---|
| Category | Architecture |
| Probability | 3 (confirmed) |
| Impact | 2 |
| Score | 6 (High) |
| Status | MITIGATED (demo mode designed) |

**Evidence:** Repository is empty; no model artifact exists.

**Impact:** API cannot serve real predictions until training is complete. Frontend cannot demonstrate real inference.

**Mitigation:** Demo mode is a first-class architectural feature. The API is designed to report `model-not-ready` gracefully. The frontend works in demo mode without API connectivity.

---

### R-05 — No local GPU for training

| Field | Value |
|---|---|
| Category | Infrastructure |
| Probability | 3 |
| Impact | 2 |
| Score | 6 (High) |
| Status | MITIGATED (Colab planned) |

**Evidence:** Blueprint explicitly states the development laptop has no NVIDIA GPU.

**Mitigation:** All training runs in Google Colab (T4 or A100 GPU). Notebooks are designed to run in Colab environment. Checkpoints saved to Google Drive.

---

### R-06 — Annotation format unknown until dataset downloaded

| Field | Value |
|---|---|
| Category | ML / Blocker |
| Probability | 3 (information not available yet) |
| Impact | 3 (wrong format = training fails) |
| Score | 9 (Critical) |
| Status | OPEN |
| Affected phases | 2, 3 |

**Evidence:** Zenodo page gives no annotation format details. Notebook 03 is specifically designed to detect and convert annotation formats.

**Impact:** If annotations are in an unusual or proprietary format, conversion pipeline must be written before training can begin.

**Proposed mitigations:**
1. Notebook 03 inspects annotation files and detects format automatically.
2. Conversion to YOLO format is implemented for Pascal VOC XML, COCO JSON, and CSV formats.
3. If format is undocumented, contact dataset authors.

---

### R-07 — Class labels incompatible between datasets

| Field | Value |
|---|---|
| Category | ML |
| Probability | 2 |
| Impact | 3 |
| Score | 6 (High) |
| Status | OPEN |
| Affected phases | 1, 2 |

**Evidence:** Grocer-Help and Roboflow datasets were created independently. Class names, granularity, and definitions may differ significantly.

**Impact:** Merging incompatible classes silently would produce a poorly trained model that appears to work but makes category errors.

**Proposed mitigations:**
1. Do not assume compatibility. Build mapping table (Section 5 of DATASET_AND_LICENSE_AUDIT.md).
2. If exact compatibility cannot be established, train separate task-specific models.
3. Conservative approach: use only Grocer-Help for initial training, add supplementary data only if labels are verified as compatible.

---

### R-08 — Oracle Cloud free tier not available in target region

| Field | Value |
|---|---|
| Category | Infrastructure |
| Probability | 2 |
| Impact | 2 |
| Score | 4 (Medium) |
| Status | OPEN |
| Affected phases | 7 |

**Evidence:** Oracle Free Tier ARM VM availability is region-dependent and has been constrained in some regions.

**Impact:** Backend hosting may not be free if Oracle Cloud is unavailable.

**Proposed mitigations:**
1. Try multiple OCI regions (Mumbai, Hyderabad for India).
2. If OCI is unavailable, fall back to Railway.app ($5–20/month), Render.com, or Fly.io.
3. Budget $20/month for backend hosting as a contingency.

---

### R-09 — CPU inference latency too high for synchronous API

| Field | Value |
|---|---|
| Category | Performance |
| Probability | 2 |
| Impact | 2 |
| Score | 4 (Medium) |
| Status | DEFERRED (benchmark required) |

**Evidence:** YOLOv8n on CPU typically 50–300ms depending on hardware. Oracle VM has 4× Ampere A1 cores (ARM). Unknown until benchmarked.

**Impact:** If inference takes > 2 seconds, user experience is poor. Queue architecture (Celery/Redis) may be needed.

**Proposed mitigations:**
1. Benchmark YOLOv8n on Ampere A1 before committing to this platform.
2. Use YOLOv8n (smallest model) as default.
3. If latency is problematic: add async queue, or use a faster model format (ONNX, TorchScript, OpenVINO for ARM).
4. Do not add queue architecture until performance data justifies it.

---

### R-10 — Grocer-Help images not representative of VIF target stores

| Field | Value |
|---|---|
| Category | ML / Product |
| Probability | 2 |
| Impact | 3 |
| Score | 6 (High) |
| Status | OPEN |

**Evidence:** Grocer-Help is from IIT Patna — likely North Indian products and stores. VIF operates in a potentially different regional context.

**Impact:** Model may fail to detect products common in VIF stores but rare in the training set. Claimed accuracy on Grocer-Help test set may not represent actual VIF store performance.

**Proposed mitigations:**
1. During EDA (Notebook 02), inspect which Indian FMCG brands and product types are represented.
2. Supplement with VIF-specific images (custom data collection plan in IMPLEMENTATION_ROADMAP.md).
3. Never claim model accuracy without evaluating on a VIF-specific held-out set.
4. Include domain disclaimer in UI.

---

## Part 2: Architecture Decision Records

### ADR-001 — Monorepo structure

**Date:** 2026-10-17  
**Status:** Accepted

**Context:** The project has distinct ML, API, and frontend components. They share types and configuration but have different deployment targets.

**Decision:** Single monorepo with explicit subdirectories (`apps/`, `ml/`, `artifacts/`, `infra/`, `docs/`). Not a multi-repo or nx/turborepo-managed monorepo in MVP.

**Rationale:** Simpler for a small team. Shared context (types, configs) are easy to find. Can migrate to turborepo if workspace complexity grows.

**Consequences:** Single git history for all components. Deployment is per-service despite shared repo.

---

### ADR-002 — PyTorch + Ultralytics YOLO as primary ML stack

**Date:** 2026-10-17  
**Status:** Accepted (conditional on annotation compatibility)

**Context:** Multiple object detection frameworks exist (Ultralytics YOLO, Detectron2, MMDetection, PaddleDetection). The project must run in Colab.

**Decision:** Use Ultralytics (YOLOv8/v11) as primary framework.

**Rationale:**
- Easiest Colab setup (single `pip install ultralytics`).
- Supports COCO and custom datasets natively.
- Model export to ONNX, TorchScript is built-in.
- Strong community, frequent updates.
- YOLOv8n/s are efficient for CPU inference.

**Conditions:** If Grocer-Help annotations are in a format incompatible with Ultralytics dataset loading, conversion pipeline is required (Notebook 03).

---

### ADR-003 — FastAPI over Flask or Django

**Date:** 2026-10-17  
**Status:** Accepted

**Decision:** Use FastAPI for the inference service.

**Rationale:**
- Native Pydantic v2 validation (same library used for schema definitions).
- Async support natively.
- Auto-generated OpenAPI docs.
- Better type safety than Flask.
- Less overhead than Django for a focused inference service.

---

### ADR-004 — Next.js 14 App Router

**Date:** 2026-10-17  
**Status:** Accepted

**Decision:** Use Next.js 14 with App Router.

**Rationale:** Modern React patterns, server components for performance, strong Vercel integration, TypeScript-first. App Router is the current Next.js standard.

**Note:** The blueprint specifies Next.js. This decision aligns with it.

---

### ADR-005 — No authentication in MVP

**Date:** 2026-10-17  
**Status:** Accepted (revisit in Release 2)

**Decision:** No user accounts or authentication in MVP.

**Rationale:**
- Adding real authentication requires backend security, session management, and JWT/OAuth — significant complexity.
- MVP is a single-tenant tool for initial VIF evaluation.
- Decorative login buttons are explicitly prohibited by the project blueprint.

**Risk:** Analysis history is not private in MVP. All users see all analyses.

**Revisit trigger:** If multiple users or stores are onboarded, authentication is required in Release 2.

---

### ADR-006 — Demo mode as client-side toggle, not server state

**Date:** 2026-10-17  
**Status:** Accepted

**Decision:** Demo mode is controlled by a frontend environment variable / client-side toggle.

**Rationale:**
- Demo mode must work without API connectivity (for offline demos).
- Keeps the API simple and stateless.
- Clear separation: demo data is bundled in the frontend, real data comes from the API.

**Risk:** Demo data must be kept current with the API response schema.

---

### ADR-007 — No Celery/Redis in MVP

**Date:** 2026-10-17  
**Status:** Accepted (deferred, not permanently excluded)

**Decision:** MVP uses synchronous inference only. No background job queue.

**Rationale:** Premature complexity. Must benchmark actual CPU inference latency before adding queue. YOLOv8n may be fast enough for single-image uploads.

**Revisit trigger:** If synchronous inference latency > 2 seconds at p95 for expected concurrent users.

---

*Risk register version 0.1.0 — updated each phase.*
