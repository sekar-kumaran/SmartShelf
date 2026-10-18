"""
Pytest configuration and test client fixture for VIF SmartShelf API.
"""
import io
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.main import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def dummy_shelf_image_bytes():
    """Generates an in-memory 640x480 RGB test image."""
    img = Image.new("RGB", (640, 480), color=(230, 230, 230))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()
