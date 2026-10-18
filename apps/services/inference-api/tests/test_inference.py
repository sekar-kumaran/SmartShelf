"""
Tests for inference and catalog endpoints.
"""


def test_predict_endpoint_valid_image(client, dummy_shelf_image_bytes):
    response = client.post(
        "/api/v1/predict",
        files={"file": ("shelf_sample.jpg", dummy_shelf_image_bytes, "image/jpeg")},
        data={"confidence": 0.25, "iou": 0.45},
    )
    assert response.status_code == 200
    data = response.json()
    assert "audit_id" in data
    assert data["image_width"] == 640
    assert data["image_height"] == 480
    assert data["total_items_detected"] > 0
    assert "shelf_tiers" in data
    assert "brand_breakdown" in data
    assert "planogram_compliance_score" in data
    assert data["planogram_compliance_score"] >= 0.0


def test_predict_invalid_file_type(client):
    response = client.post(
        "/api/v1/predict",
        files={"file": ("not_an_image.txt", b"plain text data", "text/plain")},
    )
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]


def test_catalog_endpoint(client):
    response = client.get("/api/v1/catalog?limit=20")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert len(data["items"]) == 20
    assert "categories" in data


def test_catalog_search(client):
    response = client.get("/api/v1/catalog?q=maggi")
    assert response.status_code == 200
    data = response.json()
    for item in data["items"]:
        assert "maggi" in item["name"].lower()


def test_sample_shelves(client):
    response = client.get("/api/v1/sample-shelves")
    assert response.status_code == 200
    assert "samples" in response.json()


def test_audits_endpoint(client):
    response = client.get("/api/v1/audits")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3
