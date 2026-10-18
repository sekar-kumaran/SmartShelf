"""
VIF SmartShelf — Inference & Shelf Intelligence API Endpoints
"""
import io
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List
from fastapi import APIRouter, File, Form, UploadFile, HTTPException, Query, status
from PIL import Image

from app.core.config import get_settings
from app.schemas.detection import ShelfAnalysisResponse
from app.services.detector import ShelfDetector
from app.services.shelf_intelligence import ShelfIntelligence

router = APIRouter()


@router.post("/predict", response_model=ShelfAnalysisResponse, status_code=status.HTTP_200_OK)
async def predict_shelf(
    file: UploadFile = File(..., description="Shelf photo (JPEG/PNG/WebP)"),
    confidence: Optional[float] = Form(0.25, ge=0.01, le=1.0, description="Confidence threshold"),
    iou: Optional[float] = Form(0.45, ge=0.01, le=1.0, description="NMS IOU threshold"),
):
    """
    Run product recognition and inventory intelligence on an uploaded kirana shelf image.
    Returns:
    - Bounding boxes and labels for each detected product
    - Inferred shelf rows/tiers
    - Out-of-stock void gaps
    - Brand facing distribution
    - Shelf occupancy percentage and planogram compliance score
    """
    settings = get_settings()

    # Content type check
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file.content_type}. Please upload an image (JPEG/PNG/WebP).",
        )

    # Read bytes and validate size
    contents = await file.read()
    if len(contents) > settings.max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Image size exceeds maximum limit of {settings.max_upload_size_mb} MB.",
        )

    try:
        image = Image.open(io.BytesIO(contents))
        image.load()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Corrupt or unreadable image file: {str(e)}",
        )

    w, h = image.size
    detector = ShelfDetector.get_instance()
    raw_detections, elapsed_ms = detector.predict(
        image, conf_threshold=confidence, iou_threshold=iou
    )

    (
        clustered_detections,
        shelf_tiers,
        void_gaps,
        brand_breakdown,
        occupancy_pct,
        compliance_score,
    ) = ShelfIntelligence.analyze_shelf(raw_detections, image_width=w, image_height=h)

    unique_skus = len(set(d.class_id for d in clustered_detections))

    return ShelfAnalysisResponse(
        audit_id=f"audit_{uuid.uuid4().hex[:12]}",
        timestamp=datetime.now(timezone.utc).isoformat(),
        image_width=w,
        image_height=h,
        total_items_detected=len(clustered_detections),
        unique_skus_detected=unique_skus,
        estimated_shelf_occupancy_pct=occupancy_pct,
        shelf_tiers=shelf_tiers,
        detections=clustered_detections,
        out_of_stock_gaps=void_gaps,
        brand_breakdown=brand_breakdown,
        planogram_compliance_score=compliance_score,
        inference_time_ms=elapsed_ms,
        model_version=settings.model_version,
    )


@router.get("/sample-shelves")
async def list_sample_shelves():
    """
    Returns a list of sample shelf image paths from the Indian Grocery dataset
    to enable instant 1-click test inference in the web frontend.
    """
    candidates = [
        Path("Grocery_Items.v45i.yolo26/test/images"),
        Path("../../Grocery_Items.v45i.yolo26/test/images"),
        Path("d:/smartshelf/Grocery_Items.v45i.yolo26/test/images"),
    ]
    samples = []
    for c in candidates:
        if c.exists():
            img_files = list(c.glob("*.jpg"))[:6]
            for img in img_files:
                samples.append({
                    "id": img.stem,
                    "filename": img.name,
                    "path": str(img.resolve()),
                    "label": f"Kirana Shelf Test {len(samples) + 1}"
                })
            break
    return {"samples": samples}
