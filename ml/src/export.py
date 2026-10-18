"""
VIF SmartShelf — Model Export Utility
Exports trained YOLO model to ONNX, TorchScript, or TensorRT for ultra-low latency edge/server inference.
"""
import argparse
import sys
from pathlib import Path


def export_model(weights_path: str, export_format: str = "onnx", imgsz: int = 640, half: bool = False):
    try:
        from ultralytics import YOLO
    except ImportError:
        print("Ultralytics not installed. Install with `pip install ultralytics`.")
        sys.exit(1)

    weights = Path(weights_path)
    if not weights.exists():
        print(f"Weights file not found: {weights}")
        sys.exit(1)

    print(f"Exporting {weights} to format '{export_format}' (imgsz={imgsz}, half={half})...")
    model = YOLO(str(weights))
    exported_path = model.export(
        format=export_format,
        imgsz=imgsz,
        half=half,
        dynamic=True,
        simplify=True,
    )
    print(f"Successfully exported to: {exported_path}")
    return exported_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export VIF SmartShelf YOLO model")
    parser.add_argument("--weights", default="artifacts/models/smartshelf/best.pt", help="Path to best.pt")
    parser.add_argument("--format", default="onnx", choices=["onnx", "torchscript", "engine"], help="Export format")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size")
    parser.add_argument("--half", action="store_true", help="FP16 half-precision")
    args = parser.parse_args()

    export_model(args.weights, args.format, args.imgsz, args.half)
