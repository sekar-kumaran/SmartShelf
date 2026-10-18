"""
VIF SmartShelf — YOLO Polygon to Bounding Box Converter
Converts variable-length polygon annotations (class x1 y1 x2 y2 ...) to
standard YOLO object detection bounding boxes (class xc yc w h),
clamped to [0.0, 1.0].
"""
from pathlib import Path
import sys
import yaml


def polygon_to_bbox(coords: list[float]) -> tuple[float, float, float, float]:
    """Convert a flat list of x1, y1, x2, y2, ... to (xc, yc, w, h)."""
    xs = coords[0::2]
    ys = coords[1::2]
    min_x = max(0.0, min(xs))
    max_x = min(1.0, max(xs))
    min_y = max(0.0, min(ys))
    max_y = min(1.0, max(ys))

    w = max(0.001, max_x - min_x)
    h = max(0.001, max_y - min_y)
    xc = min_x + w / 2.0
    yc = min_y + h / 2.0
    return round(xc, 6), round(yc, 6), round(w, 6), round(h, 6)


def convert_dataset_annotations(dataset_root: Path, output_root: Path = None):
    """
    Reads labels from dataset_root (train/valid/test), converts any polygon lines
    to standard YOLO bounding box format. If output_root is None, updates in-place or creates standard_labels.
    """
    splits = ["train", "valid", "test"]
    total_converted = 0
    total_kept = 0

    for split in splits:
        lbl_dir = dataset_root / split / "labels"
        if not lbl_dir.exists():
            continue

        out_lbl_dir = (output_root / split / "labels") if output_root else lbl_dir
        out_lbl_dir.mkdir(parents=True, exist_ok=True)

        for lbl_file in lbl_dir.glob("*.txt"):
            new_lines = []
            modified = False
            with open(lbl_file, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split()
                    if not parts:
                        continue
                    cls_id = parts[0]
                    coords = [float(x) for x in parts[1:]]

                    if len(coords) == 4:
                        # Already standard YOLO (xc, yc, w, h)
                        new_lines.append(f"{cls_id} {' '.join(parts[1:])}")
                        total_kept += 1
                    elif len(coords) > 4:
                        # Polygon format! Convert to bounding box
                        xc, yc, w, h = polygon_to_bbox(coords)
                        new_lines.append(f"{cls_id} {xc} {yc} {w} {h}")
                        modified = True
                        total_converted += 1
                    else:
                        continue

            if modified or output_root:
                with open(out_lbl_dir / lbl_file.name, "w", encoding="utf-8") as f:
                    f.write("\n".join(new_lines) + "\n")

    print(f"Annotation normalization complete! Kept standard bbox: {total_kept:,}, Converted polygons: {total_converted:,}")


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent.parent
    data_dir = root / "Grocery_Items.v45i.yolo26"
    print(f"Normalizing annotations in {data_dir}...")
    convert_dataset_annotations(data_dir)
