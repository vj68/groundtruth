from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "GroundTruth"
    environment: str = "development"
    google_cloud_project: str = "groundtruth-507213"
    google_cloud_location: str = "global"
    model: str = "gemini-3.5-flash"
    use_vertex: bool = True
    enable_gemini: bool = True
    use_firestore: bool = False
    firestore_collection: str = "groundtruth-runs"
    artifact_dir: Path = Path("artifacts/runs")
    fixture_dir: Path = Path("fixtures")
    demo_delay_ms: int = 350


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.artifact_dir.mkdir(parents=True, exist_ok=True)
    return settings
