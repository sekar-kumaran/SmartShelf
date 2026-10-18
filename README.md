# VIF SmartShelf

**Indian Retail Shelf Vision, Product Recognition and Inventory Intelligence**

> 🚧 **Status: Phase 0 — Audit Complete, Implementation In Progress**  
> This project is under active development. See [IMPLEMENTATION_ROADMAP.md](docs/IMPLEMENTATION_ROADMAP.md) for current status.

---

## Overview

VIF SmartShelf is a computer-vision system designed to assist Indian kirana store owners, grocery employees, and retail inventory managers in identifying products on shelves, counting visible products, and detecting possible empty or understocked areas — from uploaded shelf photographs.

**Core principle:** This system provides model-estimated detections to assist human review. It does not claim to replace manual inventory verification or provide exact stock counts. All predictions are clearly labelled as model estimates.

---

## Target Users

- Indian kirana shop owners
- Grocery store employees
- Retail inventory managers
- Small supermarkets
- Future: VIF and NearMart integration partners

---

## Capabilities (MVP)

| Feature | Status |
|---|---|
| Image upload and validation | 🔲 Not started |
| YOLO-based shelf object detection | 🔲 Blocked (no model yet) |
| Bounding box visualisation | 🔲 Not started |
| Product counting by category | 🔲 Blocked (no model yet) |
| Analysis history | 🔲 Not started |
| Demo mode | 🔲 Not started |
| Model health status | 🔲 Not started |

See [PROJECT_BLUEPRINT.md](docs/PROJECT_BLUEPRINT.md) for full feature classification and roadmap.

---

## Repository Structure

```
vif-smartshelf/
├── apps/
│   ├── web/                         # Next.js 14 frontend (TypeScript + Tailwind CSS)
│   └── services/
│       └── inference-api/           # FastAPI inference service (Python 3.11)
├── ml/
│   ├── notebooks/                   # Google Colab notebooks (00-10)
│   ├── configs/                     # YOLO training config YAML files
│   └── src/                         # Python ML utilities
├── artifacts/
│   └── models/smartshelf/           # Released model metadata (NOT binary weights)
├── infra/
│   ├── docker/                      # Dockerfiles
│   └── deployment/                  # Nginx, systemd, and cloud configs
├── docs/                            # All project documentation
├── reports/                         # Generated data analysis reports
├── .github/workflows/               # CI/CD workflows
├── docker-compose.yml               # Local development
├── Makefile                         # Developer commands
└── .env.example                     # Environment variable template
```

---

## Quick Start (Local Development)

> **Prerequisites:** Docker Desktop, Node.js 20+, Python 3.11+

```bash
# 1. Clone the repository
git clone https://github.com/your-org/vif-smartshelf.git
cd vif-smartshelf

# 2. Copy and edit environment variables
cp .env.example .env
# Edit .env with your configuration

# 3. Start the database
docker compose up -d db

# 4. Run database migrations
make db-migrate

# 5. Start the inference API
make api-dev

# 6. Start the frontend (in a new terminal)
make web-dev

# Open http://localhost:3000
```

> **Note:** The API will start in `model-not-ready` state if `best.pt` is not present.  
> `/health/ready` will return 503. Demo mode on the frontend will still work.  
> See [DEPLOYMENT_PLAN.md](docs/DEPLOYMENT_PLAN.md) for model artifact setup.

---

## Google Colab ML Workflow

Training requires a Google Colab session with GPU. Local GPU is not required.

```
ml/notebooks/
├── 00_environment_and_setup.ipynb
├── 01_dataset_acquisition_and_integrity.ipynb
├── 02_dataset_eda.ipynb
├── 03_annotation_validation_and_conversion.ipynb
├── 04_dataset_splitting_and_preprocessing.ipynb
├── 05_yolo_baseline_training.ipynb
├── 06_model_evaluation.ipynb
├── 07_error_analysis_and_tuning.ipynb
├── 08_final_model_training.ipynb
├── 09_model_export_and_inference_validation.ipynb
└── 10_deployment_smoke_tests.ipynb
```

See [MODEL_TRAINING.md](docs/MODEL_TRAINING.md) for detailed instructions.

**Dataset access required:** See [DATASET_AND_LICENSE_AUDIT.md](docs/DATASET_AND_LICENSE_AUDIT.md) for dataset access instructions. The primary dataset (Grocer-Help) requires a Zenodo account.

---

## Documentation

| Document | Purpose |
|---|---|
| [PROJECT_AUDIT.md](docs/PROJECT_AUDIT.md) | Repository audit findings |
| [PROJECT_BLUEPRINT.md](docs/PROJECT_BLUEPRINT.md) | Product vision and feature spec |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture and ADRs |
| [IMPLEMENTATION_ROADMAP.md](docs/IMPLEMENTATION_ROADMAP.md) | Phased plan and acceptance criteria |
| [DATASET_AND_LICENSE_AUDIT.md](docs/DATASET_AND_LICENSE_AUDIT.md) | Dataset access, licenses, class mappings |
| [DEPLOYMENT_PLAN.md](docs/DEPLOYMENT_PLAN.md) | Full deployment guide |
| [RISKS_AND_DECISIONS.md](docs/RISKS_AND_DECISIONS.md) | Risk register and ADRs |

---

## Technology Stack

| Layer | Technology |
|---|---|
| ML framework | PyTorch + Ultralytics YOLO |
| Training | Google Colab (T4/A100 GPU) |
| Backend API | FastAPI 0.115 + Python 3.11 |
| Database | PostgreSQL 16 (Alembic migrations) |
| Frontend | Next.js 14 · TypeScript · Tailwind CSS |
| Containerisation | Docker + Docker Compose |
| Frontend hosting | Vercel |
| Backend hosting | Oracle Cloud VM (ARM) |
| Model storage | Hugging Face Hub |
| CI/CD | GitHub Actions |

---

## Model Limitations

The current model (when trained) will have the following known limitations:

- Trained on a limited set of Indian retail product categories.
- Accuracy degrades with heavy occlusion, unusual lighting, and very small products.
- Cannot identify individual SKUs or exact product brands from the current training data.
- Shelf occupancy estimation is experimental and may be unreliable.
- Not evaluated on VIF-specific store imagery — accuracy in VIF stores is unknown until evaluated.

All predictions include confidence scores. Low-confidence detections are flagged with a warning.

---

## Datasets

| Dataset | Role | License | Access |
|---|---|---|---|
| [Grocer-Help](https://zenodo.org/records/10464054) | Primary training | CC-BY 4.0 | Restricted (Zenodo login required) |
| [Indian Grocery (Roboflow)](https://universe.roboflow.com/agentsk47/indian-grocery-object-detection-mfsnx) | Supplementary | Unknown (verify before use) | Requires Roboflow account |
| SKU-110K | Not used (license unclear) | Research only | Excluded |

---

## Contributing

This project follows a phased development protocol. Before contributing:

1. Read [ARCHITECTURE.md](docs/ARCHITECTURE.md).
2. Check [IMPLEMENTATION_ROADMAP.md](docs/IMPLEMENTATION_ROADMAP.md) for current phase.
3. Do not add features that are not in the current phase scope.
4. Do not fabricate test results or metrics.

---

## License

Application code: MIT License (see LICENSE file — to be added).  
Trained model artifacts: See [DATASET_AND_LICENSE_AUDIT.md](docs/DATASET_AND_LICENSE_AUDIT.md) for dataset-derived license requirements.

---

*VIF SmartShelf — Phase 0 complete. Next: Phase 1 Dataset Verification.*
