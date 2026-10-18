"""
VIF SmartShelf — FastAPI Application Entry Point
Production-ready Computer Vision & Inventory Intelligence Service.
"""
import time
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.api.v1.api import api_router
from app.services.detector import ShelfDetector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("smartshelf.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logger.info(f"Starting VIF SmartShelf API v{settings.app_version} ({settings.app_env})")
    # Pre-warm detector
    detector = ShelfDetector.get_instance()
    logger.info(f"Detector initialized with {len(detector.classes)} grocery classes.")
    yield
    logger.info("Shutting down VIF SmartShelf API.")


settings = get_settings()

app = FastAPI(
    title="VIF SmartShelf — Retail Vision & Inventory Intelligence API",
    description=(
        "Computer-vision application for Indian kirana stores, supermarkets, "
        "and FMCG operations. Powered by YOLO trained on 1,816 Indian grocery SKUs."
    ),
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits local development on any port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{process_time * 1000.0:.2f}ms"
    return response


# Mount API Router
app.include_router(api_router)

# Mount sample images if available
sample_images_dir = Path("d:/smartshelf/Grocery_Items.v45i.yolo26/test/images")
if not sample_images_dir.exists():
    sample_images_dir = Path("Grocery_Items.v45i.yolo26/test/images")

if sample_images_dir.exists():
    app.mount("/static/samples", StaticFiles(directory=str(sample_images_dir)), name="samples")
    logger.info(f"Mounted sample images from {sample_images_dir} at /static/samples")


@app.get("/", tags=["Root"])
async def root():
    return {
        "service": "VIF SmartShelf Inference API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health/ready",
        "sample_predict": "/api/v1/predict",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
