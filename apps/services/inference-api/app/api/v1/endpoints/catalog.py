"""
VIF SmartShelf — Grocery Product Catalog API
Provides instant search, pagination, and category filtering across 1,816 Indian FMCG SKUs.
"""
from typing import Optional, List
from fastapi import APIRouter, Query
from app.schemas.detection import CatalogItem
from app.services.detector import ShelfDetector

router = APIRouter()


@router.get("/catalog", response_model=dict)
async def get_catalog(
    q: Optional[str] = Query(None, description="Search term for product name"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(50, ge=1, le=200, description="Items per page"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
):
    detector = ShelfDetector.get_instance()
    all_classes = detector.classes

    items: List[CatalogItem] = []
    for idx, name in enumerate(all_classes):
        cat = detector._categorize_product(name)
        popular = idx in [46, 773, 192, 1187, 1204, 1317, 1094, 217, 1386, 291]
        items.append(CatalogItem(class_id=idx, name=name, category=cat, popular=popular))

    filtered = items
    if q:
        query_str = q.lower().strip()
        filtered = [item for item in filtered if query_str in item.name.lower()]

    if category:
        cat_str = category.lower().strip()
        filtered = [item for item in filtered if cat_str in item.category.lower()]

    total_count = len(filtered)
    paginated = filtered[offset : offset + limit]

    categories = sorted(list(set(item.category for item in items)))

    return {
        "total": total_count,
        "offset": offset,
        "limit": limit,
        "categories": categories,
        "items": paginated,
    }
