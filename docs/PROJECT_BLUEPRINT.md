# VIF SmartShelf — Project Blueprint

**Version:** 0.1.0  
**Date:** 2026-10-17  
**Status:** Phase 0 — Audit Complete, Implementation Not Started

---

## 1. Project Identity

**Name:** VIF SmartShelf  
**Category:** Deep learning · Computer vision · Retail intelligence · Inventory assistance  
**Organisation:** VIF (associated with NearMart ecosystem)  
**Target market:** Indian kirana stores, grocery chains, FMCG inventory managers, small supermarkets

---

## 2. Core Problem Statement

Indian retailers need to:
- Identify products on shelves from photographs.
- Count visible products per category.
- Detect possible empty or understocked shelf areas.
- Perform these tasks faster and more consistently than manual inspection.

**VIF SmartShelf** provides computer-vision assistance for these workflows from uploaded shelf images.

### Fundamental Principle

> Never present an unverified prediction as ground truth. Clearly distinguish model detections, estimated shelf occupancy, actual inventory records, and business recommendations.

---

## 3. Primary Users

| User | Context | Core Need |
|---|---|---|
| Kirana shop owner | Small neighbourhood store | Quickly photograph shelf, know what's there |
| Grocery store employee | Mid-size retail | Identify restocking priority from aisle photo |
| Inventory manager | Supermarket chain | Track shelf presence across multiple visits |
| Future: VIF integration | SmartPOS / SmartStock | API-level shelf data for larger system |

---

## 4. Technical Stack (Decided)

### ML
- Framework: PyTorch + Ultralytics YOLO (YOLOv8/v11)
- Training environment: Google Colab (T4 or A100 GPU)
- Primary dataset: Grocer-Help (pending access)
- Annotation format: YOLO (conversion may be required)

### Backend
- Language: Python 3.11+
- Framework: FastAPI
- Database: PostgreSQL (Alembic migrations)
- Image processing: Pillow, OpenCV
- Model serving: Ultralytics inference, loaded at startup

### Frontend
- Framework: Next.js 14 (App Router)
- Language: TypeScript
- Styling: Tailwind CSS
- UI components: Custom + Shadcn/ui
- State: React Query (server state) + Zustand (client state)

### Infrastructure
- Local dev: Docker Compose
- Backend hosting: Oracle Cloud (free-tier ARM VM) or equivalent
- Frontend hosting: Vercel
- Database: Neon (managed PostgreSQL, free tier)
- Model storage: Hugging Face Hub or Cloudflare R2
- CI/CD: GitHub Actions

---

## 5. VIF Design System

| Token | Value | Usage |
|---|---|---|
| `--color-surface-primary` | `hsl(222, 47%, 8%)` | Page background |
| `--color-surface-card` | `hsl(222, 35%, 13%)` | Card backgrounds |
| `--color-surface-elevated` | `hsl(222, 30%, 18%)` | Modal, dropdown backgrounds |
| `--color-accent-pink` | `#ff007f` | CTA buttons, active states |
| `--color-accent-blue` | `hsl(210, 100%, 60%)` | Links, info states |
| `--color-text-primary` | `hsl(210, 20%, 96%)` | Headings, primary text |
| `--color-text-secondary` | `hsl(215, 15%, 65%)` | Secondary labels |
| `--color-border` | `hsl(222, 25%, 22%)` | Card borders |
| Font primary | Inter (Google Fonts) | Body, UI elements |
| Font mono | JetBrains Mono | Code, confidence values |

**Accent colour: pink `#ff007f`. Do NOT use orange as primary accent.**

---

## 6. Feature Classification

| Feature | Phase | Status |
|---|---|---|
| Image upload + validation | MVP | Not started |
| YOLO object detection | MVP | Blocked (no model) |
| Bounding box visualisation | MVP | Not started |
| Product counting | MVP | Blocked (no model) |
| Analysis results display | MVP | Not started |
| Demo mode | MVP | Not started |
| Analysis history | MVP | Not started |
| Health / model status | MVP | Not started |
| Shelf occupancy estimate | Release 2 | Not started |
| CSV/PDF export | Release 2 | Not started |
| Manual review / correction | Release 2 | Not started |
| SmartPOS integration | Release 3 | Not started |
| Batch processing | Release 4 | Not started |
| GPU serving | Release 4 | Conditional |

---

## 7. Supported Inference Tasks (Version 0.1)

| Task | ID | Description | Supported in MVP |
|---|---|---|---|
| Shelf object detection | Task A | Detect objects on shelf, return bounding boxes | YES (when model trained) |
| Product category recognition | Task B | Classify detected objects into categories | PARTIAL (depends on labels) |
| Exact product/brand recognition | Task C | Identify specific SKUs or brands | DEFERRED — requires fine-grained labels |
| Product counting | Task D | Count instances by class | YES |
| Shelf occupancy estimation | Task E | Estimate occupied/empty shelf fraction | EXPERIMENTAL |
| Inventory/stockout assistance | Task F | Alert on possible gaps | DEFERRED — requires assortment data |

---

## 8. Model Input/Output Contract

### Input
- Image file: JPEG, PNG, or WebP
- Max file size: 10 MB (configurable)
- Min dimensions: 100 × 100 px
- Max dimensions: 8,000 × 8,000 px (server-side resize to model input)
- Model input size: 640 × 640 (YOLOv8/11 default, configurable)

### Output (Detection response schema)
```json
{
  "analysis_id": "uuid",
  "model_version": "smartshelf-v0.1.0",
  "task_type": "shelf_detection",
  "image_width": 1920,
  "image_height": 1080,
  "detections": [
    {
      "detection_id": "uuid",
      "class_id": 0,
      "class_name": "product",
      "confidence": 0.87,
      "bounding_box": {
        "x_min": 120,
        "y_min": 340,
        "x_max": 280,
        "y_max": 460,
        "convention": "pixel_absolute_xyxy"
      }
    }
  ],
  "total_detected_objects": 42,
  "counts_by_class": {
    "product": 42
  },
  "shelf_occupancy": null,
  "processing_time_ms": 245,
  "warnings": ["Low confidence on 3 detections. Review recommended."],
  "created_at": "2026-10-17T13:40:00Z"
}
```

Bounding box convention: **pixel-absolute x_min, y_min, x_max, y_max (xyxy)**. Coordinates are guaranteed within image boundaries.

---

## 9. Demo Mode Specification

Demo mode must:
- Use pre-computed sample outputs (not live model inference).
- Display a prominent `DEMO MODE` banner on every page.
- Never mix demo metrics with real user analyses.
- Work without backend credentials.
- Clearly label all displayed data as sample data.

Real inference mode must:
- Use the deployed FastAPI service.
- Display genuine model outputs.
- Show model version and known limitations.
- Handle model unavailability gracefully (never fall back to fabricated predictions silently).

---

## 10. Definition of MVP

The MVP is shippable when:
1. One validated shelf-detection model is trained and its artifact is published.
2. Image upload and result display work end-to-end.
3. Bounding boxes and product counts are shown.
4. Demo mode works without API connectivity.
5. Health endpoints accurately reflect model readiness.
6. Error states are handled on all pages.
7. The application is deployed (or deployable) per the documented deployment plan.
8. Model limitations are clearly communicated on the UI.

---

*Blueprint version 0.1.0 — update when major decisions change.*
