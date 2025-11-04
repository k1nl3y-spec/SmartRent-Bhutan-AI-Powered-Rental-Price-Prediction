"""Configuration management for the SmartRent Bhutan API."""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Application configuration loaded from defaults or environment."""

    project_name: str = "SmartRent Bhutan API"
    api_version: str = "0.2.0"
    model_version: str = "1.0.0"
    model_path: Path = Path("models/rental_price_model.joblib")
    training_data_path: Path = Path("data/rental_listings.csv")


@lru_cache
def get_settings() -> Settings:
    """Return a cached instance of :class:`Settings`."""

    return Settings()
