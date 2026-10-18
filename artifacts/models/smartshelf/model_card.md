# VIF SmartShelf — Model Card

## Model Details
- **Model Name:** VIF SmartShelf Retail Vision Detector (v0.1.0)
- **Architecture:** YOLOv8 (Ultralytics) with modified anchor-free head and PAN-FPN neck
- **Task:** Multiclass Object Detection & Shelf Facing Intelligence
- **Classes:** 1,816 Indian Kirana / Supermarket FMCG SKUs
- **Input Resolution:** 640 x 640 x 3 (RGB)
- **Supported Backends:** PyTorch (`.pt`), ONNX Runtime (`.onnx`), TensorRT (`.engine`)

## Training Data
- **Dataset:** Grocery Items v45i (Roboflow Universe / IIT Patna)
- **License:** Public Domain
- **Total Images:** 5,983 (Train: 4,922, Valid: 750, Test: 311)
- **Total Annotations:** 76,306 normalized retail product bounding boxes
- **Key Categories:** Amul dairy, Haldirams namkeen, Britannia biscuits, Maggi noodles, Catch spices, Cadbury confectionery, hygiene & toiletries (Dettol, Lifebuoy, Colgate, Sensodyne).

## Intended Use
- **Primary:** Automated Kirana store & supermarket inventory counting, planogram compliance, out-of-stock void detection, and brand facing analysis.
- **Secondary:** Visual check-out assistance, stock audit validation, distributor shelf verification.
- **Out of Scope:** Person tracking, biometric identification, surveillance without user consent.

## Metrics & Benchmark Goals
| Metric | Benchmark Target |
|---|---|
| mAP@0.50 | ≥ 0.72 |
| mAP@0.50:0.95 | ≥ 0.54 |
| Facing Count Accuracy | ≥ 92% |
| CPU Latency (640x640) | < 120 ms |
| GPU Latency (T4/RTX) | < 18 ms |

## Ethical Considerations & Bias
- Dataset is sourced from Indian retail setups, optimized for regional packaging (Hindi/English dual-script, regional brands, pouch packaging, loose hanging chips/biscuits).
- Performance under extremely dim Kirana illumination is augmented via HSV jitter, but optimal results require at least 150 lux ambient store lighting.
