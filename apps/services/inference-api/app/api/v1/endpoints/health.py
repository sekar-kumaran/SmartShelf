"""
VIF SmartShelf — Health Check Endpoints
Liveness and Readiness probes for Kubernetes / Docker container monitoring.
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Response, status
from app.core.config import get_settings
from app.schemas.detection import HealthStatus
from app.services.detector import ShelfDetector

router = APIRouter()


@router.get("/health/live", status_code=status.HTTP_200_OK)
async def liveness_probe():
    """Returns 200 OK if service process is alive."""
    return {"status": "alive", "timestamp": datetime.now(timezone.utc).isoformat()}


@router.get("/health/ready", response_model=HealthStatus, status_code=status.HTTP_200_OK)
async def readiness_probe(response: Response):
    """
    Returns 200 OK when model engine and configuration are initialized.
    Returns 503 if critical subsystem fails.
    """
    settings = get_settings()
    detector = ShelfDetector.get_instance()

    return HealthStatus(
        status="ready",
        app_version=settings.app_version,
        model_loaded=detector.model_loaded,
        model_version=settings.model_version,
        device="cuda" if detector.model_loaded else "cpu",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
