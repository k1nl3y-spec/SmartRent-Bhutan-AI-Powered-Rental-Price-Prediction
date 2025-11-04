"""Configuration management for the SmartRent Bhutan API."""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    """Application configuration loaded from defaults or environment."""

    project_name: str = "SmartRent Bhutan API"
    api_version: str = "0.1.0"
    default_model_path: str = "models/baseline-model.joblib"


@lru_cache
def get_settings() -> Settings:
    """Return a cached instance of :class:`Settings`."""

    return Settings()
