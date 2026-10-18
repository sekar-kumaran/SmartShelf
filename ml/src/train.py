"""
VIF SmartShelf — Model Training Pipeline
Uses Ultralytics YOLO to train a state-of-the-art detector on the Indian Grocery dataset.
Logs metrics, saves checkpoints, and prepares artifacts for deployment.
"""
import argparse
import sys
from pathlib import Path
import yaml


def train_model(config_path: str, data_path: str = None, epochs: int = None, batch: int = None, device: str = None):
    try:
        from ultralytics import YOLO
    except ImportError:
        print("Ultralytics not installed. Install with `pip install ultralytics`.")
        sys.exit(1)

    cfg_file = Path(config_path)
    if not cfg_file.exists():
        print(f"Config file not found: {cfg_file}")
        sys.exit(1)

    with open(cfg_file, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # Overrides
    epochs = epochs or cfg["training"]["epochs"]
    batch = batch or cfg["training"]["batch_size"]
    device = device if device is not None else cfg["training"]["device"]
    data_yaml = data_path or cfg["dataset"]["data_yaml"]
    model_name = cfg["model"]["architecture"]

    print(f"=== Starting VIF SmartShelf YOLO Training ===")
    print(f"Base model: {model_name}")
    print(f"Data configuration: {data_yaml}")
    print(f"Epochs: {epochs}, Batch size: {batch}, Device: {device}")

    model = YOLO(model_name)

    results = model.train(
        data=data_yaml,
        epochs=epochs,
        batch=batch,
        imgsz=cfg["dataset"]["imgsz"],
        device=device,
        optimizer=cfg["training"]["optimizer"],
        lr0=cfg["training"]["lr0"],
        lrf=cfg["training"]["lrf"],
        weight_decay=cfg["training"]["weight_decay"],
        warmup_epochs=cfg["training"]["warmup_epochs"],
        patience=cfg["training"]["patience"],
        save_period=cfg["training"]["save_period"],
        amp=cfg["training"]["amp"],
        hsv_h=cfg["augmentation"]["hsv_h"],
        hsv_s=cfg["augmentation"]["hsv_s"],
        hsv_v=cfg["augmentation"]["hsv_v"],
        degrees=cfg["augmentation"]["degrees"],
        translate=cfg["augmentation"]["translate"],
        scale=cfg["augmentation"]["scale"],
        mosaic=cfg["augmentation"]["mosaic"],
        mixup=cfg["augmentation"]["mixup"],
        flipud=cfg["augmentation"]["flipud"],
        fliplr=cfg["augmentation"]["fliplr"],
        project="artifacts/training_runs",
        name="smartshelf_run",
        exist_ok=True,
    )

    print("=== Training Complete ===")
    best_weights = Path("artifacts/training_runs/smartshelf_run/weights/best.pt")
    if best_weights.exists():
        target_dir = Path("artifacts/models/smartshelf")
        target_dir.mkdir(parents=True, exist_ok=True)
        import shutil
        target_file = target_dir / "best.pt"
        shutil.copy2(best_weights, target_file)
        print(f"Copied best weights to {target_file}")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VIF SmartShelf Training")
    parser.add_argument("--config", default="ml/configs/smartshelf_yolov8.yaml", help="Path to YAML training config")
    parser.add_argument("--data", default=None, help="Path to data.yaml override")
    parser.add_argument("--epochs", type=int, default=None, help="Number of epochs override")
    parser.add_argument("--batch", type=int, default=None, help="Batch size override")
    parser.add_argument("--device", default=None, help="Device (cpu, 0, etc.)")
    args = parser.parse_args()

    train_model(args.config, args.data, args.epochs, args.batch, args.device)
