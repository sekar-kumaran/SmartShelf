"""
Tests for shelf spatial clustering and void gap detection logic.
"""
from app.schemas.detection import DetectionItem, BoundingBox
from app.services.shelf_intelligence import ShelfIntelligence


def test_shelf_spatial_clustering():
    # 2 rows of 3 items each
    items = [
        # Row 1 (y around 100)
        DetectionItem(
            id="1", class_id=46, class_name="Amul", confidence=0.9,
            bbox=BoundingBox(x1=50, y1=100, x2=150, y2=200, width=100, height=100)
        ),
        DetectionItem(
            id="2", class_id=46, class_name="Amul", confidence=0.88,
            bbox=BoundingBox(x1=160, y1=105, x2=260, y2=205, width=100, height=100)
        ),
        # Gap on Row 1 (next item at x=450 instead of 270)
        DetectionItem(
            id="3", class_id=46, class_name="Amul", confidence=0.92,
            bbox=BoundingBox(x1=450, y1=102, x2=550, y2=202, width=100, height=100)
        ),
        # Row 2 (y around 350)
        DetectionItem(
            id="4", class_id=773, class_name="Maggi", confidence=0.85,
            bbox=BoundingBox(x1=50, y1=350, x2=150, y2=450, width=100, height=100)
        ),
        DetectionItem(
            id="5", class_id=773, class_name="Maggi", confidence=0.87,
            bbox=BoundingBox(x1=160, y1=355, x2=260, y2=455, width=100, height=100)
        ),
    ]

    dets, tiers, gaps, brand_shares, occ, score = ShelfIntelligence.analyze_shelf(
        items, image_width=800, image_height=600
    )

    assert len(tiers) == 2
    assert tiers[0].row == 1
    assert tiers[0].item_count == 3
    assert tiers[1].row == 2
    assert tiers[1].item_count == 2
    # Verify void gap was detected on row 1
    assert len(gaps) >= 1
    assert gaps[0].shelf_row == 1
    assert gaps[0].bbox.x1 == 262.0  # 260 + 2
    assert gaps[0].bbox.x2 == 448.0  # 450 - 2
