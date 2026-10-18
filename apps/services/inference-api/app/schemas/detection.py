"""
VIF SmartShelf — Pydantic Schemas for Detections and Shelf Intelligence
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    x1: float = Field(..., description="Top-left X coordinate (pixels or normalized)")
    y1: float = Field(..., description="Top-left Y coordinate (pixels or normalized)")
    x2: float = Field(..., description="Bottom-right X coordinate (pixels or normalized)")
    y2: float = Field(..., description="Bottom-right Y coordinate (pixels or normalized)")
    width: float = Field(..., description="Box width")
    height: float = Field(..., description="Box height")


class DetectionItem(BaseModel):
    id: str = Field(..., description="Unique detection ID")
    class_id: int = Field(..., description="Numeric class index (0-1815)")
    class_name: str = Field(..., description="Indian FMCG product/brand name")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Detection confidence score")
    bbox: BoundingBox
    shelf_row: Optional[int] = Field(None, description="Inferred shelf tier (1 = top shelf)")
    category: Optional[str] = Field("General Grocery", description="Broader FMCG category")


class ShelfVoidGap(BaseModel):
    shelf_row: int = Field(..., description="Shelf tier containing the void gap")
    bbox: BoundingBox = Field(..., description="Estimated empty shelf space")
    severity: str = Field("warning", description="Severity: warning | critical")
    message: str = Field("Potential out-of-stock gap detected", description="User alert description")


class BrandShare(BaseModel):
    brand: str
    count: int
    percentage: float


class ShelfTierSummary(BaseModel):
    row: int
    item_count: int
    sku_count: int
    dominant_brand: Optional[str] = None
    occupancy_percentage: float


class ShelfAnalysisResponse(BaseModel):
    audit_id: str
    timestamp: str
    image_width: int
    image_height: int
    total_items_detected: int
    unique_skus_detected: int
    estimated_shelf_occupancy_pct: float
    shelf_tiers: List[ShelfTierSummary]
    detections: List[DetectionItem]
    out_of_stock_gaps: List[ShelfVoidGap]
    brand_breakdown: List[BrandShare]
    planogram_compliance_score: float = Field(..., ge=0.0, le=100.0)
    inference_time_ms: float
    model_version: str


class HealthStatus(BaseModel):
    status: str
    app_version: str
    model_loaded: bool
    model_version: str
    device: str
    timestamp: str


class CatalogItem(BaseModel):
    class_id: int
    name: str
    category: str
    popular: bool = False
