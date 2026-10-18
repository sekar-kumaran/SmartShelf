# VIF SmartShelf — Dataset & Annotation Format Inspection Report

**Generated Date:** 2026-10-17  
**Dataset:** Grocery_Items.v45i.yolo26  
**License:** Public Domain (Roboflow / IIT Patna)  

---

## 1. Executive Summary

- **Total Images:** 5,983
- **Total Split Distribution:**
  - **Train:** 4,922 images (62,747 annotations)
  - **Validation:** 750 images (9,462 annotations)
  - **Test:** 311 images (4,097 annotations)
- **Total Defined Classes:** 1,816
- **Classes with at least 1 instance:** 1,816
- **Corrupt / Unreadable Images:** 0 (100% data integrity)

---

## 2. Annotation Formats Detected

The dataset uses a hybrid YOLO format:
{
  "standard_bbox_5_val": 62130,
  "polygon_segmentation": 14176
}

- `standard_bbox_5_val`: Standard YOLO format `[class_id, x_center, y_center, width, height]`
- `polygon_segmentation`: Polygon segmentations `[class_id, x1, y1, x2, y2, ...]` containing bounding vertices.
- **Action Taken:** An automated converter (`ml/src/convert_annotations.py`) calculates the minimum bounding box encompassing all polygon vertices for standard YOLOv8/v10/v11 bounding box object detection training.

---

## 3. Top 15 Most Frequent Grocery Products

| Class ID | Product / SKU Name | Instance Count |
|---|---|---|
| 1204 | SoftDrink | 3177 |
| 1187 | Soap | 2874 |
| 444 | DrOetker | 2220 |
| 773 | Maggi | 2125 |
| 1317 | ToothPaste | 2102 |
| 1083 | Real | 1886 |
| 1053 | Pulses | 1710 |
| 46 | Amul | 1572 |
| 1094 | RedLabel | 1478 |
| 192 | Britannia | 1421 |
| 291 | Chings | 1302 |
| 1386 | Vim | 1225 |
| 217 | Cadbury | 1105 |
| 1375 | Veeba | 883 |
| 1269 | TajMahal | 863 |

---

## 4. Top Image Resolutions

| Resolution (WxH) | Frequency |
|---|---|
| 1080x1920 | 1211 |
| 500x500 | 874 |
| 4000x3000 | 808 |
| 4032x3024 | 377 |
| 4160x3120 | 219 |

---

## 5. Verification Status

- [x] All 5,983 image files parsed without decode errors.
- [x] All label files present with valid integers and floating-point coordinates.
- [x] Class names represent authentic Indian Kirana & supermarket goods (Amul, Haldirams, Parle, Catch, Britannia, etc.).
- [x] Public Domain license verified in `README.dataset.txt`.
