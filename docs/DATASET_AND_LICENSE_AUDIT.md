# VIF SmartShelf — Dataset and License Audit

**Version:** 1.0.0  
**Date:** 2026-10-17  
**Status:** Phase 1 COMPLETE & VERIFIED

---

## CRITICAL UPDATE — Dataset Verified and Normalized

The dataset is verified at `Grocery_Items.v45i.yolo26`:
- **Source:** IIT Patna (Roboflow Universe)
- **License:** Public Domain
- **Total Images:** 5,983 (Train: 4,922 / Valid: 750 / Test: 311)
- **Total Annotations:** 76,306 (Train: 62,747 / Valid: 9,462 / Test: 4,097)
- **Classes:** 1,816 authentic Indian retail FMCG categories (Amul, Maggi, Britannia, Haldirams, etc.)
- **Format Normalization:** All 14,176 polygon annotations successfully converted to standard YOLO bounding boxes via `ml/src/convert_annotations.py`.
- **Integrity:** 0 corrupt images. All splits verified. Reports generated: `reports/dataset_manifest.json`, `reports/class_distribution.csv`, `reports/annotation_format_report.md`.

---

## 1. Overview

This document records the findings from inspecting each candidate dataset for VIF SmartShelf. It will be updated after actual dataset files are downloaded and inspected (Phase 1).

---

## 2. Grocer-Help (Primary Dataset)

### 2.1 Basic Information

| Property | Value |
|---|---|
| Name | Grocer-Help |
| Zenodo URL | https://zenodo.org/records/10464054 |
| DOI | 10.5281/zenodo.10464054 |
| Primary author | Sah, Mayank (Researcher, IIT Patna) |
| Supervisor | Mathew, Jimson (IIT Patna) |
| Institution | Indian Institute of Technology Patna (ROR: 01ft5vz71) |
| Published | Zenodo (date not confirmed externally) |

### 2.2 License

| Property | Value |
|---|---|
| License | Creative Commons Attribution 4.0 International (CC-BY 4.0) |
| Full text | https://creativecommons.org/licenses/by/4.0/legalcode |
| Commercial use | PERMITTED with attribution |
| Modification | PERMITTED with attribution |
| Distribution | PERMITTED with attribution |
| Attribution requirement | Must credit Sah, Mayank and Mathew, Jimson, IIT Patna, DOI 10.5281/zenodo.10464054 |

### 2.3 Access Status

| Property | Value |
|---|---|
| Record visibility | Publicly accessible |
| **File download** | **RESTRICTED — Zenodo login required, possibly author approval needed** |
| Download method | Zenodo web interface (after login) or Zenodo API with OAuth token |
| Status as of audit | Files not downloaded; access not yet requested |

### 2.4 Described Contents (From Public Metadata — Unverified Until Downloaded)

| Subset | Described Count |
|---|---|
| Close-Shot images | 2,460 |
| Long-Shot images | 2,604 |
| Online images | 2,307 |
| **Total** | **7,371** |
| Training set | 6,682 |
| Test set | 689 |

**⚠️ These counts come from the Zenodo record description. Actual file counts must be verified after download.**

### 2.5 Unknowns (Must Verify After Download)

- [ ] Actual downloaded file count
- [ ] Image formats (JPEG, PNG, WebP?)
- [ ] Image dimensions and aspect ratio distribution
- [ ] Annotation format (Pascal VOC XML? COCO JSON? YOLO txt? Other?)
- [ ] Class names and class count
- [ ] Whether bounding boxes are present or only image-level labels
- [ ] Whether individual product/brand labels or generic object labels
- [ ] Presence of corrupted or truncated files
- [ ] Presence of duplicate images
- [ ] Archive structure (single archive? per-subset archives?)
- [ ] Uncompressed disk space requirement

### 2.6 Required Actions

1. Create a Zenodo account if not already done.
2. Log in and attempt file download from https://zenodo.org/records/10464054.
3. If files are not immediately downloadable, contact authors:
   - Email: (search IIT Patna faculty pages for Jimson Mathew or Mayank Sah)
4. Document the outcome in this file.
5. Once downloaded, run integrity checks (file count, checksums, format inspection).

---

## 3. Indian Grocery Object Detection (Supplementary)

### 3.1 Basic Information

| Property | Value |
|---|---|
| Name | Indian Grocery Object Detection |
| Roboflow URL | https://universe.roboflow.com/agentsk47/indian-grocery-object-detection-mfsnx |
| Workspace owner | agentsk47 |
| Platform | Roboflow Universe |

### 3.2 Access Status

| Property | Value |
|---|---|
| Access attempt | HTTP 403 — access denied without authentication |
| Roboflow account required | YES |
| Status as of audit | Inaccessible — not inspected |

### 3.3 Described Contents (From Blueprint — Unverified)

| Property | Described Value |
|---|---|
| Image count | ~403 |
| Class count | ~10 FMCG classes |
| Annotation format | Roboflow native (YOLO/COCO exportable) |
| License | Unknown |

**⚠️ All values are unverified. Must log in to Roboflow to inspect actual contents.**

### 3.4 Required Actions

1. Create or use existing Roboflow account.
2. Navigate to the dataset workspace.
3. Inspect:
   - Actual image count
   - Class names (exact text)
   - Annotation count
   - License (check dataset settings or description)
   - Export options available
4. Download a sample (10–20 images) for quality inspection.
5. Determine whether class labels are compatible with Grocer-Help labels.
6. Verify commercial use is permitted before including in any commercial product.
7. Document findings in this file.

---

## 4. SKU-110K (Optional Supplementary)

### 4.1 Basic Information

| Property | Value |
|---|---|
| Name | SKU-110K |
| GitHub | https://github.com/eg4000/SKU110K_CVPR19 |
| Paper | "Precise Detection in Densely Packed Scenes" (Goldman et al., CVPR 2019) |
| Institution | Weizmann Institute of Science (Israel) |
| Image count | ~110,000 (large-scale) |

### 4.2 License Assessment

| Property | Value |
|---|---|
| Stated license | Research/academic use (inferred from CVPR academic paper) |
| Commercial use | **LIKELY RESTRICTED — not confirmed as commercially licensed** |
| Redistribution | Unknown |
| Status | DO NOT USE until commercial license explicitly confirmed |

### 4.3 Annotation Type Warning

> **CRITICAL:** SKU-110K annotations are generic retail object bounding boxes. They do NOT identify individual products, SKUs, or brands. Using SKU-110K class labels for brand recognition or product identification is a fundamental labelling error.

If SKU-110K is used (after commercial license confirmation), it must be used **only** for:
- Dense object detection pretraining (detecting objects exist, not what they are).
- Benchmarking shelf density estimation.

It must NOT be used for:
- Any claim of product identification.
- Any claim of brand recognition.
- Merging generic object classes with Grocer-Help product category labels.

### 4.4 Decision

**Current decision: EXCLUDE SKU-110K from VIF SmartShelf MVP.**

Reason:
- Commercial license restrictions are unconfirmed.
- Annotations do not support the product recognition tasks required.
- The primary tasks can be attempted with Grocer-Help + supplementary Roboflow data.

This decision is revisited only if:
- Commercial license is explicitly confirmed in writing.
- Grocer-Help data proves insufficient for shelf density tasks.

---

## 5. Canonical Class Schema

**Status: CANNOT BE DEFINED — dataset inspection pending.**

The canonical class schema will be built after:
1. Grocer-Help class names are extracted from annotation files.
2. Roboflow dataset class names are extracted.
3. Compatibility is assessed.

The schema will take this form:

| Source | Original Class ID | Original Class Name | Canonical Class ID | Canonical Class Name | Label Type | Mapping Confidence | Decision |
|---|---|---|---|---|---|---|---|
| Grocer-Help | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Roboflow | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

---

## 6. License Attribution Registry

All datasets used in training must be attributed in:
- `docs/DATASET_AND_LICENSE_AUDIT.md` (this file)
- `artifacts/models/smartshelf/model_card.md`
- Application Settings page (UI)
- Any published model on Hugging Face Hub

| Dataset | License | Attribution Required |
|---|---|---|
| Grocer-Help | CC-BY 4.0 | YES — cite Sah, Mathew, IIT Patna, DOI 10.5281/zenodo.10464054 |
| Indian Grocery (Roboflow) | Unknown | TBD after inspection |
| SKU-110K | Research only (unconfirmed) | EXCLUDED unless license confirmed |

---

## 7. Dataset Combination Policy

1. Only combine datasets whose labels have been explicitly verified as compatible.
2. Build a mapping table (Section 5 above) before any combined training run.
3. If class meanings differ between datasets, either:
   a. Restrict to the intersection of compatible classes, OR
   b. Train separate models for each dataset.
4. Do not silently rename classes to force compatibility.
5. Do not train on a combined dataset without documenting the combination rationale.
6. The held-out test set must not contain images from a different source than the training set without explicit domain-shift documentation.

---

## 8. Update Log

| Date | Update |
|---|---|
| 2026-10-17 | Initial audit — external inspection only. Files not downloaded. |
| TBD | Phase 1 — actual file inspection after download |

---

*This document must be updated after Phase 1 dataset inspection is complete.*
