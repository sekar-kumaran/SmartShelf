# 🚀 VIF SmartShelf — Google Colab Unified Training Guide

This guide explains how to run the full end-to-end model training, evaluation, planogram intelligence, and artifact export pipeline on **Google Colab** using the unified notebook.

---

## 📁 Notebook Location
The single unified notebook is located at:
* **Primary:** [`ml/notebooks/VIF_SmartShelf_Colab_Unified_Pipeline.ipynb`](file:///d:/smartshelf/ml/notebooks/VIF_SmartShelf_Colab_Unified_Pipeline.ipynb)
* **Mirror:** [`ml/notebooks/smartshelf_training.ipynb`](file:///d:/smartshelf/ml/notebooks/smartshelf_training.ipynb)

Both files contain the complete 27-cell workflow ready for Google Colab.

---

## ⚡ 3-Step Execution on Google Colab

### Step 1: Open Google Colab & Upload Notebook
1. Navigate to **[colab.research.google.com](https://colab.research.google.com)** in your web browser.
2. In the dialog, select **Upload** tab.
3. Choose `VIF_SmartShelf_Colab_Unified_Pipeline.ipynb` from `d:\smartshelf\ml\notebooks\`.
4. Ensure GPU runtime is active:
   * Click **Runtime > Change runtime type**
   * Hardware accelerator: **T4 GPU** (free tier) or **A100 GPU** (Colab Pro)
   * Click **Save**

---

### Step 2: Provide the Dataset (Choose Any 1 Option)

#### Option A: Google Drive (Recommended)
1. Zip your local dataset folder:
   ```powershell
   Compress-Archive -Path "d:\smartshelf\Grocery_Items.v45i.yolo26" -DestinationPath "d:\smartshelf\Grocery_Items.v45i.yolo26.zip"
   ```
2. Upload `Grocery_Items.v45i.yolo26.zip` to your Google Drive root or inside a `smartshelf/` folder.
3. When Cell 2.1 runs in Colab, grant permission to mount Google Drive. The notebook automatically detects and unpacks the zip.

#### Option B: Direct Upload to Colab
1. In Colab's left sidebar, click the 📁 **Files** icon.
2. Drag and drop `Grocery_Items.v45i.yolo26.zip` into the `/content/` area.
3. The notebook will automatically find it and extract it.

#### Option C: Direct Download via Roboflow
* If you set your `ROBOFLOW_API_KEY`, the notebook will automatically fetch version 45 of `iit-patna-qg1jh/grocery_items-7i2em` directly into the Colab environment.

---

### Step 3: Run All Cells
* Click **Runtime > Run all** (or press `Ctrl+F9`).
* The notebook executes all phases:
  1. **Phase 1:** Environment verification & dependency installation (`ultralytics`, `torch`, `onnx`, etc.)
  2. **Phase 2:** Annotation normalization (automatically converts polygon coordinates to standard YOLO `[xc, yc, w, h]` bounding boxes)
  3. **Phase 3:** Visual inspection of ground truth shelf items & 1,816 SKU class verification
  4. **Phase 4:** Retail-tuned YOLO training with Kirana lighting augmentations and AdamW optimizer
  5. **Phase 5:** Test split evaluation (`mAP@50`, `mAP@50:95`, precision, recall, latency)
  6. **Phase 6:** Visual Planogram Intelligence Demo (Shelf Tier Clustering, Facing Counts, Out-of-Stock void detection)
  7. **Phase 7:** ONNX model export, TorchScript export, rich `sku_catalog.json` generation, and automatic packaging into `vif_smartshelf_production_bundle.zip`

---

## 📦 Deploying Trained Weights to your Local SmartShelf App

When the notebook completes, Cell 7.3 triggers an automatic browser download of:
```
vif_smartshelf_production_bundle.zip
```

### To use these weights in your running app:
1. Extract the downloaded `vif_smartshelf_production_bundle.zip`.
2. Copy `best.pt` and `best.onnx` into:
   ```
   d:\smartshelf\artifacts\models\smartshelf\
   ```
3. Restart your local FastAPI backend:
   ```powershell
   cd d:\smartshelf\apps\services\inference-api
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
4. Open the Web Application at **`http://localhost:3000/`**.
5. Upload any shelf image in the **Vision Inspector** to see real-time bounding boxes, category tags, facing counts, and out-of-stock gap alerts!
