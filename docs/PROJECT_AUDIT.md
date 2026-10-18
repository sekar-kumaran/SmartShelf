# VIF SmartShelf — Project Audit Report

**Audit Date:** 2026-10-17  
**Auditor:** Principal Engineer (AI Agent)  
**Audit Type:** Greenfield — No prior codebase found  
**Repository Root:** `d:\smartshelf`  
**Audit Status:** COMPLETE

---

## 1. Executive Summary

The repository at `d:\smartshelf` was **completely empty** at the time of audit. This is a **greenfield project** — no prior source code, notebooks, models, datasets, documentation, configuration, or deployment artefacts exist. Every component must be created from scratch.

This audit therefore shifts focus to:

1. Documenting what *must* be built (capability inventory).
2. Auditing external dataset availability, licenses, and access restrictions.
3. Identifying risks and blockers before implementation begins.
4. Establishing the architecture and phased plan.

---

## 2. Repository State at Audit Time

| Category | Finding | Severity |
|---|---|---|
| Source code | None present | INFO |
| Frontend | None present | INFO |
| Backend / API | None present | INFO |
| ML notebooks | None present | INFO |
| Trained model weights | None present | INFO |
| Datasets | None present | INFO |
| Annotation files | None present | INFO |
| Configuration files | None present | INFO |
| Tests | None present | INFO |
| CI/CD workflows | None present | INFO |
| Deployment config | None present | INFO |
| Documentation | None present | INFO |
| `.gitignore` | None present | LOW |
| `README.md` | None present | LOW |
| `docker-compose.yml` | None present | LOW |

**Conclusion:** No prior work exists. No risk of overwriting working code. No duplicate implementations. No broken imports. No dead code.

---

## 3. Dataset Access Audit

### 3.1 Grocer-Help (Primary Dataset)

| Property | Finding |
|---|---|
| URL | https://zenodo.org/records/10464054 |
| DOI | 10.5281/zenodo.10464054 |
| Authors | Sah, Mayank (IIT Patna) · Mathew, Jimson (Supervisor) |
| License | Creative Commons Attribution 4.0 International (CC-BY 4.0) |
| Public record | YES — record is publicly accessible |
| **File access** | **RESTRICTED — login required to download files** |
| Described image count | 7,371 total (2,460 close-shot · 2,604 long-shot · 2,307 online) |
| Described train/test split | 6,682 train · 689 test |
| Annotation format | Unknown — must inspect after access |
| Classes | Unknown — must inspect after access |
| Commercial use | CC-BY 4.0 permits commercial use with attribution |

**BLOCKER (HIGH):** Files are restricted. The dataset cannot be downloaded without a Zenodo account and potentially without author approval. This must be resolved before any notebook training can run.

**Action required:**
- Request dataset access via Zenodo login.
- Contact authors (Mayank Sah, IIT Patna) if direct access is not granted automatically.
- Document the outcome in `docs/DATASET_AND_LICENSE_AUDIT.md`.
- Do not proceed to training notebooks until access is confirmed.

### 3.2 Indian Grocery Object Detection (Supplementary)

| Property | Finding |
|---|---|
| URL | https://universe.roboflow.com/agentsk47/indian-grocery-object-detection-mfsnx |
| Access attempt | HTTP 403 — access denied without authentication |
| Described size | ~403 images, ~10 FMCG classes |
| Annotation format | Roboflow native (likely YOLO-format exportable) |
| License | Unknown — must authenticate to verify |
| Commercial use | Unknown |

**BLOCKER (MEDIUM):** The Roboflow dataset requires authentication. Class names, actual image count, annotation quality, and license must all be verified before using this dataset.

**Action required:**
- Create a Roboflow account and inspect the dataset workspace.
- Verify license before using in any commercial context.
- Use only as supplementary data if labels are compatible with Grocer-Help.

### 3.3 SKU-110K (Optional Supplementary)

| Property | Finding |
|---|---|
| URL | https://github.com/eg4000/SKU110K_CVPR19 |
| Repository | Public on GitHub |
| Paper | CVPR 2019 (Goldman et al.) |
| Dataset host | Separate download link (not in-repo) |
| License | **Academic/research use only — commercial restrictions apply** |
| Annotation type | Generic dense object bounding boxes (NOT individual SKU/brand labels) |
| Image count | ~110,000 (hence SKU-110K) |

**RISK (HIGH):** SKU-110K annotations are generic bounding boxes, not product/SKU labels. Using these for brand recognition or SKU identification would be a fundamental labelling error. Additionally, commercial licensing is likely restricted.

**Action required:**
- Do NOT include SKU-110K unless commercial licensing is explicitly verified.
- If included, use only for dense shelf-object detection pretraining, not class-level recognition.
- Clearly document in the class mapping table.

---

## 4. Identified Risks and Blockers

| ID | Risk | Severity | Impact | Mitigation |
|---|---|---|---|---|
| R-01 | Grocer-Help files are restricted | HIGH | No primary training data | Request Zenodo access; contact authors |
| R-02 | Roboflow dataset access denied | MEDIUM | No supplementary labelled data | Create Roboflow account; verify license |
| R-03 | SKU-110K commercial licensing unclear | HIGH | Legal risk if used commercially | Verify license; avoid until confirmed |
| R-04 | No trained model artifact exists | HIGH | API cannot serve predictions at launch | Colab training must complete first; demo mode required |
| R-05 | No GPU available locally | MEDIUM | Cannot train on developer machine | Use Google Colab T4/A100 |
| R-06 | Annotation format unknown | HIGH | Cannot confirm YOLO compatibility | Must inspect after dataset access |
| R-07 | Class mapping across datasets unknown | HIGH | May not be combinable | Must inspect both datasets' class labels |
| R-08 | No .gitignore — risk of committing large files | LOW | Git repo bloat; secret exposure | Create .gitignore before first commit |
| R-09 | No dependency pins yet | LOW | Reproducibility failure | Pin deps in requirements.txt / pyproject.toml |

---

## 5. Capability Inventory (What Must Be Built)

### ML Pipeline
- [ ] Dataset acquisition and integrity notebook
- [ ] EDA notebook
- [ ] Annotation validation and conversion notebook
- [ ] Dataset splitting and preprocessing notebook
- [ ] Baseline YOLO training notebook (Colab)
- [ ] Model evaluation notebook
- [ ] Error analysis and tuning notebook
- [ ] Final model training notebook
- [ ] Model export and inference validation notebook
- [ ] Deployment smoke-test notebook

### Backend / Inference API
- [ ] FastAPI service
- [ ] Image validation middleware
- [ ] YOLO model loader (startup, not per-request)
- [ ] Inference pipeline (preprocess -> infer -> postprocess)
- [ ] Detection API endpoint
- [ ] Shelf analysis endpoint
- [ ] Health endpoints (live + ready)
- [ ] Analysis history (PostgreSQL)
- [ ] Rate limiting and upload safety

### Frontend
- [ ] Next.js 14 application (TypeScript, Tailwind CSS)
- [ ] Landing page
- [ ] Dashboard
- [ ] Image analysis (upload + result)
- [ ] Detection review (bounding box overlay)
- [ ] Shelf occupancy display
- [ ] Analysis history
- [ ] Reports
- [ ] Settings
- [ ] Demo mode / real mode switch

### Infrastructure
- [ ] Dockerfile (backend)
- [ ] Dockerfile (frontend)
- [ ] docker-compose.yml (local dev)
- [ ] PostgreSQL migrations (Alembic)
- [ ] GitHub Actions CI workflows
- [ ] Deployment configuration

---

## 6. No Destructive Changes Required

Since the repository is empty, no existing working code exists to preserve. The audit confirms:

- No pages to avoid replacing.
- No working inference pipelines to protect.
- No trained models to avoid overwriting.
- No databases with live data.

Implementation may proceed once the phased plan is accepted.

---

## 7. Immediate Next Steps (Phase 0 Completion)

1. DONE  Audit complete — this document.
2. DONE  Produce PROJECT_BLUEPRINT.md, ARCHITECTURE.md, IMPLEMENTATION_ROADMAP.md.
3. DONE  Produce DATASET_AND_LICENSE_AUDIT.md.
4. DONE  Produce DEPLOYMENT_PLAN.md, RISKS_AND_DECISIONS.md.
5. TODO  Initialize repository with .gitignore, README.md, Makefile.
6. MANUAL Developer must request Grocer-Help dataset access on Zenodo.
7. MANUAL Developer must verify Roboflow dataset license.
8. TODO  Phase 1 — Dataset verification (after access confirmed).

---

*This document must be updated after every phase.*
