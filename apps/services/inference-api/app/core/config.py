"""
VIF SmartShelf — Application Configuration
Loaded from environment variables with .env fallback.
"""
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        protected_namespaces=("settings_",),
    )

    # Application
    app_env: str = "development"
    log_level: str = "INFO"
    app_version: str = "0.1.0"

    # Model
    model_artifact_path: Path = Path("/app/models/smartshelf/best.pt")
    model_version: str = "v0.1.0"
    model_sha256: str = ""  # Empty = skip checksum in dev
    hf_model_repo: str = ""  # If set, download from HF Hub on startup

    # Inference
    inference_confidence_threshold: float = 0.25
    inference_iou_threshold: float = 0.45
    inference_image_size: int = 640
    max_upload_size_mb: int = 10

    # Database
    database_url: str = (
        "postgresql+asyncpg://smartshelf:smartshelf@localhost:5432/smartshelf"
    )

    # CORS
    cors_allowed_origins: str = "http://localhost:3000"

    # Rate limiting
    rate_limit_per_minute: int = 30

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_allowed_origins.split(",")]

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
