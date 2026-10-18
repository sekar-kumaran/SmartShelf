# VIF SmartShelf — Implementation Roadmap

**Version:** 0.1.0  
**Date:** 2026-10-17  
**Status:** Active

---

## Summary

| Phase | Name | Status | Blocker |
|---|---|---|---|
| 0 | Repository Audit and Architecture | COMPLETE | None |
| 1 | Dataset Verification | COMPLETE | None (Verified from IIT Patna Roboflow dataset) |
| 2 | Notebook Pipeline | COMPLETE | None (Colab notebook & training pipeline ready) |
| 3 | Model Evaluation and Release | IN PROGRESS | None |
| 4 | FastAPI Inference Service | IN PROGRESS | None |
| 5 | Frontend Application | IN PROGRESS | None |
| 6 | Persistence and Optional Queue | NOT STARTED | Phase 4 complete |
| 7 | Containerisation and Deployment | NOT STARTED | Phases 4+5 complete |
| 8 | QA, Security, and Performance | NOT STARTED | Phase 7 complete |
| 9 | MVP Release | NOT STARTED | Phase 8 complete |

---

## Phase 0 — Repository Audit and Architecture

**Objective:** Understand what exists, define what must be built, establish architecture and risk register.

**Deliverables:**
- [x] `docs/PROJECT_AUDIT.md`
- [x] `docs/PROJECT_BLUEPRINT.md`
- [x] `docs/ARCHITECTURE.md`
- [x] `docs/IMPLEMENTATION_ROADMAP.md` (this file)
- [x] `docs/DATASET_AND_LICENSE_AUDIT.md`
- [x] `docs/DEPLOYMENT_PLAN.md`
- [x] `docs/RISKS_AND_DECISIONS.md`
- [x] `.gitignore`
- [x] `README.md`
- [x] `Makefile`
- [x] `docker-compose.yml` (stub — full services added in Phase 7)

**Acceptance Criteria:**
- [x] Existing implementation is understood (empty repository confirmed)
- [x] Critical unknowns are documented (dataset access, annotation format, licensing)
- [x] No unnecessary destructive changes made
- [x] Architecture decisions recorded in ADRs

**Estimated effort:** 1 session  
**Completed:** 2026-10-17

---

## Phase 1 — Dataset Verification

**Objective:** Confirm what the datasets actually contain before writing any training code.

**Prerequisites:**
- Developer creates Zenodo account and requests Grocer-Help access.
- Developer creates Roboflow account and inspects Indian Grocery dataset.

**Deliverables:**
- `docs/DATASET_AND_LICENSE_AUDIT.md` (updated with actual inspection results)
- `reports/dataset_manifest.json`
- `reports/class_distribution.csv`
- `reports/annotation_format_report.md`

**Tasks:**
1. Download (or mount) Grocer-Help after access is granted.
2. List all files: count by split, by format, by subset (close-shot, long-shot, online).
3. Inspect annotation files: format, class IDs, class names.
4. Inspect 20–50 sample images with annotations overlaid.
5. Verify train/test split files.
6. Identify corrupted or truncated images.
7. Check for duplicate file hashes.
8. Repeat inspection for Roboflow dataset (after login).
9. Build canonical class mapping table.
10. Determine whether datasets are mergeable without label confusion.
11. Select the model task supported by the available labels.
12. Record disk space usage.

**Acceptance Criteria:**
- Dataset manifest exists with actual file counts.
- Annotation format is identified (e.g., Pascal VOC XML, YOLO txt, COCO JSON).
- Class mapping table is complete.
- License and attribution requirements are documented.
- A defensible initial model task is selected.
- No fabricated metrics or counts.

**Estimated effort:** 1–2 sessions (after dataset access)  
**BLOCKED ON:** Zenodo dataset access request

---

## Phase 2 — Notebook Pipeline

**Objective:** Create the full Google Colab notebook workflow for data preparation, training, and evaluation.

**Prerequisites:** Phase 1 complete (dataset downloaded, annotation format known).

**Notebooks to deliver:**
| File | Purpose |
|---|---|
| `ml/notebooks/00_environment_and_setup.ipynb` | GPU check, deps, config |
| `ml/notebooks/01_dataset_acquisition_and_integrity.ipynb` | Download, verify, extract |
| `ml/notebooks/02_dataset_eda.ipynb` | EDA with visualisations |
| `ml/notebooks/03_annotation_validation_and_conversion.ipynb` | Validate + convert to YOLO |
| `ml/notebooks/04_dataset_splitting_and_preprocessing.ipynb` | Splits, augmentation config |
| `ml/notebooks/05_yolo_baseline_training.ipynb` | Baseline training (Colab GPU) |
| `ml/notebooks/06_model_evaluation.ipynb` | Metrics, confusion matrix |
| `ml/notebooks/07_error_analysis_and_tuning.ipynb` | Error analysis, hyperparameter search |
| `ml/notebooks/08_final_model_training.ipynb` | Best config, full training |
| `ml/notebooks/09_model_export_and_inference_validation.ipynb` | Export + validate artifact |
| `ml/notebooks/10_deployment_smoke_tests.ipynb` | Load artifact, validate API schema |

**Acceptance Criteria:**
- Each notebook has a clear purpose, instructions, and validation cells.
- Dataset paths use configurable variables (no hardcoded paths).
- Training can run in Colab with T4 GPU.
- No fabricated metrics in outputs.
- Baseline can be trained within a single Colab session limit.

**Estimated effort:** 2–3 sessions

---

## Phase 3 — Model Evaluation and Release

**Objective:** Train, evaluate, select, and release a validated model artifact.

**Prerequisites:** Phase 2 notebooks complete and runnable in Colab.

**Tasks:**
1. Run baseline training (Notebook 05).
2. Evaluate on validation set (Notebook 06).
3. Run error analysis (Notebook 07).
4. Tune configuration based on error analysis findings.
5. Run final training with best config (Notebook 08).
6. Evaluate against held-out test set.
7. Export model artifact (Notebook 09).
8. Publish to Hugging Face Hub (or Cloudflare R2).
9. Create model card and evaluation summary.
10. Verify deployment smoke tests pass (Notebook 10).

**Acceptance Criteria:**
- Held-out test set evaluation is documented with actual numbers.
- Failure examples are reviewed and documented.
- Artifact includes: `best.pt`, `model_metadata.json`, `class_mapping.json`, `evaluation_summary.json`, `model_card.md`, `SHA256SUMS.txt`.
- Inference works outside training notebook (verified in Notebook 10).
- Release readiness explicitly stated.

**Estimated effort:** 2–4 sessions (Colab training time varies)

---

## Phase 4 — FastAPI Inference Service

**Objective:** Implement the production inference API.

**Prerequisites:** Phase 3 model artifact published and checksum verified.

**Tasks:**
1. Scaffold FastAPI project in `apps/services/inference-api/`.
2. Implement model loader with startup validation.
3. Implement image validation middleware.
4. Implement preprocessing pipeline.
5. Implement inference pipeline.
6. Implement `/health/live` and `/health/ready`.
7. Implement `/api/v1/model/info`.
8. Implement `POST /api/v1/detections`.
9. Implement `POST /api/v1/shelf-analysis`.
10. Implement analysis history endpoints.
11. Set up PostgreSQL + Alembic migrations.
12. Write unit tests (mocked model).
13. Write integration tests (real model artifact).

**Acceptance Criteria:**
- Model loads from versioned artifact (not hardcoded path).
- Health endpoints accurately reflect readiness.
- Invalid inputs return 4xx with clear error messages.
- Valid images produce correctly structured responses matching the API contract.
- No model training during any user request.
- Tests pass.

**Estimated effort:** 2–3 sessions

---

## Phase 5 — Frontend Application

**Objective:** Build the Next.js 14 frontend.

**Prerequisites:** Phase 4 API contract is finalised. Model artifact available (for real-mode testing). Demo data prepared.

**Pages to implement:**
- Landing page
- Dashboard
- Image analysis + detection review
- Shelf occupancy
- Analysis history
- Reports (MVP: CSV export)
- Settings

**Acceptance Criteria:**
- Upload, prediction display, and error states work.
- Demo mode clearly labelled and separate from real mode.
- VIF design system applied consistently.
- No dead primary actions.
- Responsive on mobile (375px) and desktop (1280px+).
- Bounding box canvas overlay renders correctly.

**Estimated effort:** 3–4 sessions

---

## Phase 6 — Persistence and Optional Queue

**Objective:** Ensure analysis history persists correctly, and evaluate whether background job queue is needed.

**Tasks:**
1. Verify PostgreSQL migrations run cleanly in Docker.
2. Verify history endpoints paginate correctly.
3. Benchmark API latency under expected load.
4. Decision: add Celery/Redis only if synchronous inference is proven insufficient.

**Acceptance Criteria:**
- Migrations work from a fresh database.
- History shows correct analyses with pagination.
- Failure and retry behaviour (if queue added) is documented.
- No false inventory facts stored.

**Estimated effort:** 1 session

---

## Phase 7 — Containerisation and Deployment

**Objective:** Package and deploy all services.

**Tasks:**
1. Write `Dockerfile` for inference API.
2. Write `Dockerfile` for frontend (or configure Vercel).
3. Write `docker-compose.yml` for local dev (frontend + API + PostgreSQL).
4. Configure Nginx reverse proxy with HTTPS.
5. Deploy API to Oracle Cloud VM.
6. Deploy frontend to Vercel.
7. Set up managed PostgreSQL (Neon).
8. Configure environment variables (no secrets in source).
9. Verify end-to-end with a real test image.

**Acceptance Criteria:**
- `docker compose up` starts all local services.
- Health checks pass on deployed services.
- HTTPS and CORS configured correctly.
- Model artifact loaded securely (checksum verified at startup).
- Secrets are absent from source control.

**Estimated effort:** 2–3 sessions

---

## Phase 8 — QA, Security, and Performance

**Objective:** Run tests, security review, and performance benchmarks.

**Tasks:**
1. Run full test suite (unit + integration + frontend).
2. Security review: upload validation, CORS, rate limiting, secret management.
3. Benchmark API latency (p50, p95) under realistic load.
4. Accessibility audit of frontend.
5. Document outstanding issues and production blockers.

**Acceptance Criteria:**
- Critical tests pass.
- Known failures are explicitly documented.
- Latency benchmarks are recorded.
- No secrets or sensitive data in logs.

**Estimated effort:** 1–2 sessions

---

## Phase 9 — MVP Release

**Objective:** Prepare MVP for use.

**Tasks:**
1. Update README with complete setup instructions.
2. Write user documentation (how to use the application).
3. Write operations runbook.
4. Document known limitations prominently.
5. Create release checklist.
6. Tag v0.1.0 in git.

**Acceptance Criteria:**
- A new developer can follow setup instructions without help.
- Application runs from documented commands.
- Model version and application version are traceable.
- Demo and real predictions are not confused.
- No known critical blockers.

**Estimated effort:** 1 session

---

## Critical Path

```
Phase 0 (audit + docs)
    └─→ MANUAL: Request Grocer-Help access
        └─→ Phase 1 (dataset verification)
            └─→ Phase 2 (notebooks)
                └─→ Phase 3 (model training + release)
                    └─→ Phase 4 (API)  ─→ Phase 5 (frontend)
                                           └─→ Phase 6 (persistence)
                                               └─→ Phase 7 (deployment)
                                                   └─→ Phase 8 (QA)
                                                       └─→ Phase 9 (release)
```

**Longest dependency chain bottleneck:** Grocer-Help dataset access → model training (Colab) → API → frontend.

---

*Roadmap version 0.1.0 — updated after each phase completion.*
