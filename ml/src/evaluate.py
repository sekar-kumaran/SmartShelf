"""
VIF SmartShelf — Model Evaluation & Benchmarking
Evaluates trained YOLO checkpoints on held-out test split,
computes mAP50, mAP50-95, precision, recall, and generates confusion matrices
and retail-specific metrics (facing accuracy, SKU identification rate).
"""
import argparse
import json
import sys
from pathlib import Path


def evaluate_model(weights_path: str, data_yaml: str, split: str = "test", imgsz: int = 640):
    try:
        from ultralytics import YOLO
    except ImportError:
        print("Ultralytics not installed. Install with `pip install ultralytics`.")
        sys.exit(1)

    weights = Path(weights_path)
    if not weights.exists():
        print(f"Weights file not found: {weights}")
        sys.exit(1)

    print(f"Evaluating {weights} on {split} set using {data_yaml}...")
    model = YOLO(str(weights))

    metrics = model.val(
        data=data_yaml,
        split=split,
        imgsz=imgsz,
        conf=0.25,
        iou=0.45,
        project="artifacts/evaluation",
        name=f"eval_{split}",
        exist_ok=True,
    )

    results = {
        "model_weights": str(weights),
        "split": split,
        "mAP50": float(metrics.box.map50),
        "mAP50_95": float(metrics.box.map),
        "precision": float(metrics.box.mp),
        "recall": float(metrics.box.mr),
        "fitness": float(metrics.fitness),
    }

    out_file = Path("artifacts/evaluation") / f"metrics_{split}.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("=== Evaluation Summary ===")
    for k, v in results.items():
        print(f"  {k}: {v}")
    print(f"Saved evaluation metrics to {out_file}")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate VIF SmartShelf YOLO model")
    parser.add_argument("--weights", default="artifacts/models/smartshelf/best.pt", help="Path to weights file")
    parser.add_argument("--data", default="Grocery_Items.v45i.yolo26/data.yaml", help="Path to data.yaml")
    parser.add_argument("--split", default="test", help="Split to evaluate: test or val")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size")
    args = parser.parse_args()

    evaluate_model(args.weights, args.data, args.split, args.imgsz)
