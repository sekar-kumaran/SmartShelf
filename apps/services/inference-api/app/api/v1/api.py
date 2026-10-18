"""
VIF SmartShelf — API v1 Router Registration
"""
from fastapi import APIRouter
from app.api.v1.endpoints import health, inference, catalog, audits

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(inference.router, prefix="/api/v1", tags=["Inference"])
api_router.include_router(catalog.router, prefix="/api/v1", tags=["Catalog"])
api_router.include_router(audits.router, prefix="/api/v1", tags=["Audits"])
