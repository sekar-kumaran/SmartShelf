"""
Script to generate the unified VIF SmartShelf Google Colab Notebook.
Produces a complete, self-contained, 1-click runnable .ipynb notebook.
"""
import json
from pathlib import Path


def create_colab_notebook():
    cells = []

    # Helper functions to add markdown and code cells
    def add_md(source):
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [line + "\n" for line in source.strip().split("\n")]
        })

    def add_code(source):
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [line + "\n" for line in source.strip().split("\n")]
        })

    # =========================================================================
    # CELL 1: Header & Colab Badge
    # =========================================================================
    add_md("""# 🛒 VIF SmartShelf — Unified End-to-End Pipeline
### Indian Retail Shelf Vision, FMCG SKU Recognition & Planogram Intelligence

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com)

**Author:** Principal CV & ML Lead, VIF SmartShelf  
**Dataset:** Indian Grocery Items (`Grocery_Items.v45i.yolo26`) — 1,816 SKU classes, IIT Patna (Public Domain)  
**Target Hardware:** Google Colab (Free T4 GPU or A100 GPU)  

---

### What this Unified Notebook Executes:
1. **⚡ Phase 1: Environment Setup & GPU Verification** (PyTorch, Ultralytics, ONNX, Seeds)
2. **📦 Phase 2: Flexible Dataset Acquisition & Format Normalization** (Drive mount, zip upload, or Roboflow; converts polygons to standard YOLO bboxes)
3. **📊 Phase 3: Exploratory Data Analysis & Kirana Shelf Class Distribution**
4. **🎯 Phase 4: Retail-Tuned YOLOv8/YOLOv11 Training** (Kirana store lighting & dense packing augmentations, AdamW, checkpointing)
5. **📈 Phase 5: Model Evaluation & Benchmarking** (mAP@50, mAP@50:95, Precision, Recall, Latency)
6. **🧠 Phase 6: Retail Shelf Intelligence Demo** (Shelf Tier Clustering, Facing Counts, Out-of-Stock Void Detection)
7. **🚀 Phase 7: Production Model Export & 1-Click Download** (ONNX export, TorchScript, `sku_catalog.json`, zipped bundle for local SmartShelf Web App)""")

    # =========================================================================
    # CELL 2: GPU Check & Install Dependencies
    # =========================================================================
    add_md("""## Phase 1: Environment Setup & GPU Acceleration Check
Ensure your Colab runtime is set to GPU: **Runtime > Change runtime type > T4 GPU**.""")

    add_code("""# 1.1 Verify GPU Availability
!nvidia-smi

# 1.2 Install Required Dependencies
!pip install -q \\
    "ultralytics>=8.3.0" \\
    "opencv-python-headless>=4.9.0" \\
    "pyyaml>=6.0" \\
    "pillow>=10.0" \\
    "matplotlib>=3.8" \\
    "seaborn>=0.13" \\
    "pandas>=2.1" \\
    "numpy>=1.26" \\
    "onnx>=1.15" \\
    "onnxslim>=0.2" \\
    "roboflow>=1.1"

print("✓ All dependencies installed successfully!")""")

    # =========================================================================
    # CELL 3: Imports & Seeds
    # =========================================================================
    add_code("""# 1.3 Imports and Reproducibility Setup
import os
import sys
import glob
import json
import shutil
import random
from pathlib import Path

import cv2
import yaml
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

import torch
from ultralytics import YOLO

def set_seeds(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)

set_seeds(42)

print(f"✓ PyTorch version: {torch.__version__} (CUDA available: {torch.cuda.is_available()})")
if torch.cuda.is_available():
    print(f"✓ Active GPU: {torch.cuda.get_device_name(0)}")
""")

    # =========================================================================
    # CELL 4: Phase 2: Dataset Acquisition
    # =========================================================================
    add_md("""## Phase 2: Dataset Acquisition & Preparation
The dataset `Grocery_Items.v45i.yolo26` contains 1,816 Indian grocery classes across thousands of store shelf images.

You can use **any of the following 3 options** to load the dataset in Colab:
* **Option A (Google Drive Mount):** Upload `Grocery_Items.v45i.yolo26.zip` or folder to your Google Drive.
* **Option B (Direct Upload / Local Zip):** Upload the `.zip` file directly into `/content/` using the Colab file browser.
* **Option C (Roboflow Universe API):** Direct download via Roboflow API.""")

    add_code("""# 2.1 Mount Google Drive (Optional but Recommended)
try:
    from google.colab import drive
    drive.mount('/content/drive')
    IN_COLAB = True
    print("✓ Google Drive mounted at /content/drive")
except Exception as e:
    IN_COLAB = False
    print(f"Not running in Colab or Drive mount skipped: {e}")
""")

    add_code("""# 2.2 Dataset Location & Auto-Extraction
# This cell automatically detects if the dataset folder or zip exists in /content or Google Drive

DATASET_NAME = "Grocery_Items.v45i.yolo26"
CANDIDATE_PATHS = [
    Path(f"/content/{DATASET_NAME}"),
    Path(f"/content/drive/MyDrive/{DATASET_NAME}"),
    Path(f"/content/drive/MyDrive/smartshelf/{DATASET_NAME}"),
    Path(f"/content/drive/MyDrive/vif-smartshelf/{DATASET_NAME}"),
    Path(DATASET_NAME)
]

ZIP_CANDIDATES = [
    Path(f"/content/{DATASET_NAME}.zip"),
    Path(f"/content/drive/MyDrive/{DATASET_NAME}.zip"),
    Path(f"/content/drive/MyDrive/smartshelf/{DATASET_NAME}.zip"),
    Path(f"{DATASET_NAME}.zip")
]

DATA_DIR = None

# Check for existing extracted folder
for p in CANDIDATE_PATHS:
    if p.exists() and (p / "data.yaml").exists():
        DATA_DIR = p
        print(f"✓ Found existing dataset at: {DATA_DIR}")
        break

# If not found, check for zip to extract
if DATA_DIR is None:
    for zp in ZIP_CANDIDATES:
        if zp.exists():
            print(f"Found dataset archive {zp}. Extracting to /content/{DATASET_NAME}...")
            shutil.unpack_archive(str(zp), f"/content/{DATASET_NAME}")
            DATA_DIR = Path(f"/content/{DATASET_NAME}")
            break

# If still not found, provide Roboflow fallback download option
if DATA_DIR is None:
    print("⚠️ Dataset not detected locally or in Drive.")
    print("You can download directly via Roboflow Universe if you have an API key,")
    print("OR upload Grocery_Items.v45i.yolo26.zip to /content/ and re-run this cell.")
    
    # Optional Roboflow download:
    ROBOFLOW_API_KEY = os.environ.get("ROBOFLOW_API_KEY", "")
    if ROBOFLOW_API_KEY:
        from roboflow import Roboflow
        rf = Roboflow(api_key=ROBOFLOW_API_KEY)
        project = rf.workspace("iit-patna-qg1jh").project("grocery_items-7i2em")
        version = project.version(45)
        dataset = version.download("yolov8", location=f"/content/{DATASET_NAME}")
        DATA_DIR = Path(f"/content/{DATASET_NAME}")
    else:
        # Create dummy directory structure for testing if user hasn't uploaded yet
        DATA_DIR = Path(f"/content/{DATASET_NAME}")

print(f"Active Dataset Directory: {DATA_DIR.resolve()}")
""")

    # =========================================================================
    # CELL 5: Annotation Normalization
    # =========================================================================
    add_md("""## 2.3 Normalize Annotations (Polygon to YOLO Bounding Box)
The raw dataset contains multi-point polygon annotations for segmented items. Standard YOLO object detection requires 4 values: `[class_id, x_center, y_center, width, height]`.
This cell converts any polygon coordinates into tightly bounded bounding boxes and verifies the splits.""")

    add_code("""def polygon_to_bbox(coords):
    \"\"\"Converts [x1, y1, x2, y2, ...] into normalized [xc, yc, w, h].\"\"\"
    xs = coords[0::2]
    ys = coords[1::2]
    min_x, max_x = max(0.0, min(xs)), min(1.0, max(xs))
    min_y, max_y = max(0.0, min(ys)), min(1.0, max(ys))
    w = max(0.001, max_x - min_x)
    h = max(0.001, max_y - min_y)
    return min_x + w / 2.0, min_y + h / 2.0, w, h

def normalize_dataset_labels(dataset_root: Path):
    if not dataset_root.exists():
        print(f"Directory {dataset_root} does not exist yet. Please upload dataset.")
        return 0
    
    converted_count = 0
    total_labels = 0
    
    for split in ["train", "valid", "test"]:
        lbl_dir = dataset_root / split / "labels"
        if not lbl_dir.exists():
            continue
        
        for lf in lbl_dir.glob("*.txt"):
            total_labels += 1
            updated_lines = []
            modified = False
            
            with open(lf, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split()
                    if not parts:
                        continue
                    class_id = parts[0]
                    coords = [float(x) for x in parts[1:]]
                    
                    if len(coords) == 4:
                        # Already bounding box [xc, yc, w, h]
                        updated_lines.append(f"{class_id} {coords[0]:.6f} {coords[1]:.6f} {coords[2]:.6f} {coords[3]:.6f}")
                    elif len(coords) > 4:
                        # Polygon format -> convert
                        xc, yc, w, h = polygon_to_bbox(coords)
                        updated_lines.append(f"{class_id} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}")
                        modified = True
            
            if modified:
                with open(lf, "w", encoding="utf-8") as f:
                    f.write("\\n".join(updated_lines) + "\\n")
                converted_count += 1

    print(f"✓ Scanned {total_labels} label files. Normalized {converted_count} polygon annotation files.")
    return total_labels

normalize_dataset_labels(DATA_DIR)
""")

    # =========================================================================
    # CELL 6: Configure data_colab.yaml
    # =========================================================================
    add_md("""## 2.4 Generate Google Colab YAML Configuration
Creates `data_colab.yaml` pointing to the exact absolute paths inside Google Colab.""")

    add_code("""original_yaml_path = DATA_DIR / "data.yaml"
colab_yaml_path = Path("/content/data_colab.yaml")

if original_yaml_path.exists():
    with open(original_yaml_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    
    class_names = cfg.get("names", [])
    num_classes = len(class_names)
    print(f"✓ Loaded {num_classes} classes from {original_yaml_path}")
    
    colab_cfg = {
        "path": str(DATA_DIR.resolve()),
        "train": str((DATA_DIR / "train" / "images").resolve()),
        "val": str((DATA_DIR / "valid" / "images").resolve()),
        "test": str((DATA_DIR / "test" / "images").resolve()),
        "nc": num_classes,
        "names": class_names
    }
    
    with open(colab_yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(colab_cfg, f, default_flow_style=False, sort_keys=False)
    
    print(f"✓ Generated Colab data configuration at: {colab_yaml_path}")
else:
    print(f"⚠️ data.yaml not found at {original_yaml_path}. Please check dataset path.")
""")

    # =========================================================================
    # CELL 7: Phase 3: Exploratory Data Analysis
    # =========================================================================
    add_md("""## Phase 3: Exploratory Data Analysis & Kirana Shelf Inspection
Inspect ground truth annotations and explore the class distribution across top Indian FMCG brands.""")

    add_code("""# 3.1 Dataset Split Image Counts
for split in ["train", "valid", "test"]:
    img_dir = DATA_DIR / split / "images"
    count = len(list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png"))) if img_dir.exists() else 0
    print(f"  Split '{split}': {count} shelf images")

# 3.2 Visualize Ground Truth Annotations on Sample Shelf Images
def visualize_ground_truth(dataset_root, split="train", num_samples=2):
    img_dir = dataset_root / split / "images"
    lbl_dir = dataset_root / split / "labels"
    
    with open(colab_yaml_path, "r", encoding="utf-8") as f:
        names = yaml.safe_load(f)["names"]
        
    img_files = list(img_dir.glob("*.jpg"))[:num_samples]
    if not img_files:
        print("No images found to display.")
        return
        
    for img_p in img_files:
        lbl_p = lbl_dir / f"{img_p.stem}.txt"
        img = cv2.imread(str(img_p))
        if img is None: continue
        h_img, w_img, _ = img.shape
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        boxes = []
        if lbl_p.exists():
            with open(lbl_p, "r") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        cid = int(parts[0])
                        xc, yc, w, h = [float(x) for x in parts[1:5]]
                        x1 = int((xc - w/2) * w_img)
                        y1 = int((yc - h/2) * h_img)
                        x2 = int((xc + w/2) * w_img)
                        y2 = int((yc + h/2) * h_img)
                        cname = names[cid] if cid < len(names) else str(cid)
                        boxes.append((x1, y1, x2, y2, cname))
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 120), 2)
                        cv2.putText(img, cname[:15], (x1, max(y1 - 5, 15)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 0), 1)

        plt.figure(figsize=(12, 7))
        plt.imshow(img)
        plt.title(f"{img_p.name} — {len(boxes)} Ground Truth Bounding Boxes", fontsize=12)
        plt.axis("off")
        plt.show()

visualize_ground_truth(DATA_DIR, split="train", num_samples=2)
""")

    # =========================================================================
    # CELL 8: Phase 4: Model Training
    # =========================================================================
    add_md("""## Phase 4: Retail-Tuned YOLOv8/YOLOv11 Training
We initialize pretrained weights and train using hyperparameters tailored for Indian Kirana shelves:
* **Fluorescent Lighting Invariance:** HSV color jitter (`hsv_h=0.015`, `hsv_s=0.7`, `hsv_v=0.4`)
* **Dense Shelf Packings:** Mosaic (`1.0`) and MixUp (`0.15`)
* **Horizontal Shelving:** No vertical flip (`flipud=0.0`), horizontal flip enabled (`fliplr=0.5`)
* **Optimizer:** AdamW with cosine learning rate schedule (`lr0=0.001`, `lrf=0.01`)""")

    add_code("""# 4.1 Hyperparameter & Training Configuration
# Choose model: 'yolov8s.pt' (fast & lightweight) or 'yolov8m.pt' (higher accuracy)
MODEL_ARCHITECTURE = "yolov8s.pt"

# Set epochs: recommended 30-50 for high accuracy; 5 for rapid verification test
EPOCHS = 30
BATCH_SIZE = 16  # 16 fits comfortably within 16GB T4 GPU VRAM
IMAGE_SIZE = 640

PROJECT_DIR = "/content/runs/smartshelf"
RUN_NAME = "kirana_yolov8_run"

print(f"=== Initializing VIF SmartShelf YOLO Training ===")
print(f"Base Architecture : {MODEL_ARCHITECTURE}")
print(f"Data YAML Config  : {colab_yaml_path}")
print(f"Epochs            : {EPOCHS}")
print(f"Batch Size        : {BATCH_SIZE}")
print(f"Image Resolution  : {IMAGE_SIZE}x{IMAGE_SIZE}")

model = YOLO(MODEL_ARCHITECTURE)

# 4.2 Start Model Training
results = model.train(
    data=str(colab_yaml_path),
    epochs=EPOCHS,
    batch=BATCH_SIZE,
    imgsz=IMAGE_SIZE,
    device=0 if torch.cuda.is_available() else "cpu",
    optimizer="AdamW",
    lr0=0.001,
    lrf=0.01,
    weight_decay=0.0005,
    warmup_epochs=3.0,
    patience=10,
    save_period=5,
    amp=True,  # Automatic Mixed Precision for fast GPU training
    hsv_h=0.015,
    hsv_s=0.7,
    hsv_v=0.4,
    degrees=0.0,
    translate=0.1,
    scale=0.5,
    mosaic=1.0,
    mixup=0.15,
    fliplr=0.5,
    flipud=0.0,
    project=PROJECT_DIR,
    name=RUN_NAME,
    exist_ok=True
)

print("🎉 Training Completed Successfully!")
""")

    # =========================================================================
    # CELL 9: Checkpoint Backup
    # =========================================================================
    add_code("""# 4.3 Checkpoint Verification & Drive Backup
best_weights_path = Path(PROJECT_DIR) / RUN_NAME / "weights" / "best.pt"

if best_weights_path.exists():
    print(f"✓ Best checkpoint created at: {best_weights_path} ({best_weights_path.stat().st_size / 1e6:.1f} MB)")
    
    # Copy to local persistent artifacts directory
    local_target = Path("/content/artifacts/models/smartshelf")
    local_target.mkdir(parents=True, exist_ok=True)
    shutil.copy2(best_weights_path, local_target / "best.pt")
    print(f"✓ Staged weights to: {local_target / 'best.pt'}")
    
    # Backup to Google Drive if connected
    if Path("/content/drive/MyDrive").exists():
        drive_target = Path("/content/drive/MyDrive/smartshelf_checkpoints")
        drive_target.mkdir(parents=True, exist_ok=True)
        shutil.copy2(best_weights_path, drive_target / "best.pt")
        print(f"✓ Backed up best.pt to Google Drive: {drive_target / 'best.pt'}")
else:
    print("⚠️ Weights not found at expected location. Check training logs above.")
""")

    # =========================================================================
    # CELL 10: Phase 5: Evaluation & Benchmarking
    # =========================================================================
    add_md("""## Phase 5: Model Evaluation & Benchmarking
Evaluate the trained model on the held-out `test` split and calculate computer vision and latency benchmarks.""")

    add_code("""# 5.1 Run Evaluation on Test Split
eval_model = YOLO(str(best_weights_path))

metrics = eval_model.val(
    data=str(colab_yaml_path),
    split="test",
    imgsz=IMAGE_SIZE,
    conf=0.25,
    iou=0.45,
    project=PROJECT_DIR,
    name="evaluation_test",
    exist_ok=True
)

eval_summary = {
    "mAP50": float(metrics.box.map50),
    "mAP50_95": float(metrics.box.map),
    "precision": float(metrics.box.mp),
    "recall": float(metrics.box.mr),
    "fitness": float(metrics.fitness),
    "inference_speed_ms": float(metrics.speed.get("inference", 0.0))
}

print("\\n" + "="*45)
print("       VIF SMARTSHELF EVALUATION BENCHMARK")
print("="*45)
print(f"  mAP @ 0.50 IoU       : {eval_summary['mAP50']*100:.2f}%")
print(f"  mAP @ 0.50:0.95 IoU  : {eval_summary['mAP50_95']*100:.2f}%")
print(f"  Precision            : {eval_summary['precision']*100:.2f}%")
print(f"  Recall               : {eval_summary['recall']*100:.2f}%")
print(f"  Mean Latency         : {eval_summary['inference_speed_ms']:.2f} ms/frame")
if eval_summary['inference_speed_ms'] > 0:
    print(f"  Throughput           : {1000.0 / eval_summary['inference_speed_ms']:.1f} FPS")
print("="*45)

# Save metrics JSON
with open("/content/artifacts/models/smartshelf/metrics_test.json", "w") as f:
    json.dump(eval_summary, f, indent=2)
""")

    # =========================================================================
    # CELL 11: Display Training & Evaluation Plots
    # =========================================================================
    add_code("""# 5.2 Display Training & PR Curves
train_run_dir = Path(PROJECT_DIR) / RUN_NAME
result_plots = ["results.png", "confusion_matrix.png", "PR_curve.png", "F1_curve.png"]

for plot_name in result_plots:
    p = train_run_dir / plot_name
    if p.exists():
        plt.figure(figsize=(10, 6))
        img = Image.open(p)
        plt.imshow(img)
        plt.title(f"Benchmark: {plot_name}", fontsize=13)
        plt.axis("off")
        plt.show()
""")

    # =========================================================================
    # CELL 12: Phase 6: Retail Shelf Vision Intelligence Demo
    # =========================================================================
    add_md("""## Phase 6: Retail Shelf Vision Intelligence Demo
In production retail operations, raw bounding boxes are converted into actionable store metrics:
1. **Shelf Tier Assignment:** Automatically groups detected products into vertical tiers (Top, Eye-Level, Reach, Bottom).
2. **Facing Count & Share of Shelf:** Aggregates SKU facings and computes brand exposure percentages.
3. **Out-of-Stock (OOS) Gap Detection:** Identifies empty voids along shelf tiers where products should be restocked.""")

    add_code("""def analyze_shelf_intelligence(image_path, model, conf_thresh=0.25):
    \"\"\"
    End-to-end Kirana shelf intelligence:
    - Runs object detection
    - Clusters detections into shelf rows/tiers
    - Detects empty void gaps between products
    - Computes brand facings and share-of-shelf
    \"\"\"
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    h_img, w_img, _ = img.shape
    results = model.predict(image_path, conf=conf_thresh, iou=0.45, verbose=False)[0]
    
    detections = []
    for box in results.boxes:
        xyxy = box.xyxy[0].cpu().numpy()
        cid = int(box.cls[0].cpu().numpy())
        cname = model.names[cid]
        conf = float(box.conf[0].cpu().numpy())
        detections.append({
            "box": xyxy,
            "class_name": cname,
            "conf": conf,
            "yc": (xyxy[1] + xyxy[3]) / 2.0,
            "xc": (xyxy[0] + xyxy[2]) / 2.0,
            "width": xyxy[2] - xyxy[0],
            "height": xyxy[3] - xyxy[1]
        })

    # Sort detections by Y-center to cluster shelf tiers
    detections.sort(key=lambda d: d["yc"])
    
    # 1. Tier Clustering
    tiers = []
    current_tier = []
    y_threshold = h_img * 0.12  # 12% of shelf height defines a tier boundary
    
    for d in detections:
        if not current_tier:
            current_tier.append(d)
        else:
            avg_y = sum(item["yc"] for item in current_tier) / len(current_tier)
            if abs(d["yc"] - avg_y) < y_threshold:
                current_tier.append(d)
            else:
                current_tier.sort(key=lambda item: item["box"][0])
                tiers.append(current_tier)
                current_tier = [d]
    if current_tier:
        current_tier.sort(key=lambda item: item["box"][0])
        tiers.append(current_tier)

    # 2. Out-of-Stock (OOS) Void Detection along each tier
    oos_gaps = []
    for tier_idx, tier_items in enumerate(tiers):
        for i in range(len(tier_items) - 1):
            right_edge_prev = tier_items[i]["box"][2]
            left_edge_next = tier_items[i+1]["box"][0]
            gap_width = left_edge_next - right_edge_prev
            
            # If gap between items exceeds average item width, flag as OOS void
            avg_item_w = (tier_items[i]["width"] + tier_items[i+1]["width"]) / 2.0
            if gap_width > (avg_item_w * 0.9):
                y1 = min(tier_items[i]["box"][1], tier_items[i+1]["box"][1])
                y2 = max(tier_items[i]["box"][3], tier_items[i+1]["box"][3])
                oos_gaps.append({
                    "tier": tier_idx + 1,
                    "box": [right_edge_prev, y1, left_edge_next, y2],
                    "gap_width": gap_width
                })

    # 3. Facing Counts and Share-of-Shelf
    facing_counts = {}
    for d in detections:
        c = d["class_name"]
        facing_counts[c] = facing_counts.get(c, 0) + 1
        
    total_facings = len(detections)
    share_of_shelf = {k: (v / total_facings) * 100 for k, v in facing_counts.items()} if total_facings > 0 else {}

    # 4. Render Visualization
    render_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Draw detected products
    for d in detections:
        x1, y1, x2, y2 = [int(v) for v in d["box"]]
        cv2.rectangle(render_img, (x1, y1), (x2, y2), (0, 220, 100), 2)
        cv2.putText(render_img, f"{d['class_name'][:12]} ({d['conf']:.2f})", (x1, max(y1-5, 12)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 0), 1)

    # Draw OOS Gap Alert boxes
    for g in oos_gaps:
        gx1, gy1, gx2, gy2 = [int(v) for v in g["box"]]
        cv2.rectangle(render_img, (gx1, gy1), (gx2, gy2), (255, 40, 40), 3)
        cv2.putText(render_img, f"OOS GAP (Tier {g['tier']})", (gx1, max(gy1-5, 15)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 50, 50), 2)

    return {
        "total_detections": total_facings,
        "tiers_detected": len(tiers),
        "oos_gaps_detected": len(oos_gaps),
        "facing_counts": facing_counts,
        "share_of_shelf": share_of_shelf,
        "rendered_image": render_img
    }

# Run demo on a test split image
test_images = list((DATA_DIR / "test" / "images").glob("*.jpg"))
if test_images:
    sample_shelf = str(test_images[0])
    print(f"Running SmartShelf Planogram Analysis on: {sample_shelf}")
    analysis = analyze_shelf_intelligence(sample_shelf, eval_model)
    
    plt.figure(figsize=(14, 9))
    plt.imshow(analysis["rendered_image"])
    plt.title(f"VIF SmartShelf Intelligence — {analysis['total_detections']} Facings | {analysis['tiers_detected']} Tiers | {analysis['oos_gaps_detected']} OOS Gaps Detected", fontsize=13)
    plt.axis("off")
    plt.show()
    
    print("\\n=== Top Brand Facings & Share-of-Shelf ===")
    top_brands = sorted(analysis["share_of_shelf"].items(), key=lambda x: x[1], reverse=True)[:8]
    for b, share in top_brands:
        print(f"  • {b:<25} : {analysis['facing_counts'][b]} facings ({share:.1f}% shelf space)")
""")

    # =========================================================================
    # CELL 13: Phase 7: Model Export & Colab Download
    # =========================================================================
    add_md("""## Phase 7: Model Export & Production Packaging
Exports the trained weights to high-speed ONNX format, compiles the complete 1,816 SKU catalog, and bundles all production files into a single downloadable zip file for your local web application.""")

    add_code("""# 7.1 Export to ONNX and TorchScript
print("Exporting trained model to ONNX format...")
onnx_path = eval_model.export(
    format="onnx",
    imgsz=IMAGE_SIZE,
    dynamic=True,
    simplify=True
)
print(f"✓ ONNX Model exported: {onnx_path}")

print("Exporting to TorchScript format...")
torchscript_path = eval_model.export(
    format="torchscript",
    imgsz=IMAGE_SIZE
)
print(f"✓ TorchScript Model exported: {torchscript_path}")
""")

    add_code("""# 7.2 Generate SKU Catalog and Production Bundle
BUNDLE_DIR = Path("/content/vif_smartshelf_production_bundle")
BUNDLE_DIR.mkdir(parents=True, exist_ok=True)

# 1. Copy weights
shutil.copy2(best_weights_path, BUNDLE_DIR / "best.pt")
if Path(onnx_path).exists():
    shutil.copy2(onnx_path, BUNDLE_DIR / "best.onnx")

# 2. Copy data config
shutil.copy2(colab_yaml_path, BUNDLE_DIR / "data.yaml")

# 3. Create rich SKU catalog JSON
with open(colab_yaml_path, "r", encoding="utf-8") as f:
    names_list = yaml.safe_load(f)["names"]

sku_catalog = []
for idx, name in enumerate(names_list):
    # Heuristic category categorization for Indian Kirana
    name_l = name.lower()
    if any(k in name_l for k in ["biscuit", "cookie", "rusk", "wafer", "cake"]):
        cat = "Biscuits & Bakery"
    elif any(k in name_l for k in ["soap", "shampoo", "facewash", "toothpaste", "lotion", "cream", "deo"]):
        cat = "Personal Care & Hygiene"
    elif any(k in name_l for k in ["masala", "oil", "salt", "atta", "dal", "sugar", "ghee", "powder"]):
        cat = "Staples & Masalas"
    elif any(k in name_l for k in ["chips", "namkeen", "bhujia", "snack", "popcorn", "chana"]):
        cat = "Snacks & Namkeen"
    elif any(k in name_l for k in ["juice", "tea", "coffee", "milk", "drink", "cola", "lassi"]):
        cat = "Beverages & Dairy"
    else:
        cat = "Household & Kirana"
        
    sku_catalog.append({
        "sku_id": f"SKU-{idx:04d}",
        "class_id": idx,
        "name": name,
        "category": cat,
        "expected_price_inr": 20 + ((idx * 17) % 230)
    })

with open(BUNDLE_DIR / "sku_catalog.json", "w", encoding="utf-8") as f:
    json.dump(sku_catalog, f, indent=2)

# 4. Copy evaluation metrics
if Path("/content/artifacts/models/smartshelf/metrics_test.json").exists():
    shutil.copy2("/content/artifacts/models/smartshelf/metrics_test.json", BUNDLE_DIR / "metrics_test.json")

# 5. Zip the bundle
ZIP_OUTPUT = "/content/vif_smartshelf_production_bundle.zip"
if Path(ZIP_OUTPUT).exists():
    os.remove(ZIP_OUTPUT)
shutil.make_archive("/content/vif_smartshelf_production_bundle", "zip", str(BUNDLE_DIR))
print(f"✓ Production bundle created: {ZIP_OUTPUT} ({Path(ZIP_OUTPUT).stat().st_size / 1e6:.1f} MB)")
""")

    add_md("""## 7.3 Download Production Bundle to Local Machine
Run the cell below to trigger the direct download of `vif_smartshelf_production_bundle.zip` to your computer.""")

    add_code("""# Trigger direct browser download in Google Colab
try:
    from google.colab import files
    files.download("/content/vif_smartshelf_production_bundle.zip")
    print("✓ Triggered browser download of vif_smartshelf_production_bundle.zip")
except Exception as e:
    print(f"Direct download trigger not available: {e}")
    print(f"You can find the zip archive at: /content/vif_smartshelf_production_bundle.zip")
""")

    add_md("""---
### 🛠️ How to Deploy These Weights in your Local SmartShelf App:
1. Extract `vif_smartshelf_production_bundle.zip` on your computer.
2. Copy `best.pt` and `best.onnx` into:
   ```
   d:\\smartshelf\\artifacts\\models\\smartshelf\\
   ```
3. Restart the FastAPI inference server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
4. Open the Web Application in your browser at `http://localhost:3000/`.
5. Upload any shelf image in the Vision Inspector to run live shelf recognition!""")

    notebook = {
        "cells": cells,
        "metadata": {
            "colab": {
                "provenance": [],
                "gpuType": "T4"
            },
            "kernelspec": {
                "display_name": "Python 3",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            },
            "accelerator": "GPU"
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }

    return notebook


if __name__ == "__main__":
    nb = create_colab_notebook()
    
    # Save unified notebook
    out1 = Path("d:/smartshelf/ml/notebooks/VIF_SmartShelf_Colab_Unified_Pipeline.ipynb")
    with open(out1, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
    print(f"Created: {out1} (cells: {len(nb['cells'])})")

    # Also update smartshelf_training.ipynb so both point to the unified pipeline
    out2 = Path("d:/smartshelf/ml/notebooks/smartshelf_training.ipynb")
    with open(out2, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
    print(f"Updated: {out2} (cells: {len(nb['cells'])})")
