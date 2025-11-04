"""Entry point for the SmartRent Bhutan FastAPI application."""
from fastapi import FastAPI

from src.api.routes import router
from src.core.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.project_name, version=settings.api_version)
app.include_router(router)
