"""Pydantic models shared across API routes."""
from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class PropertyFeatures(BaseModel):
    """Incoming request describing a property that needs a price prediction."""

    location: str = Field(..., description="Human readable location name (e.g. Thimphu)")
    location_score: float = Field(
        ..., ge=0, le=5, description="Normalized desirability score for the neighborhood."
    )
    property_type: str = Field(..., description="Apartment, house, villa, etc.")
    size_sqft: float = Field(..., gt=0, description="Total floor area measured in square feet.")
    bedrooms: int = Field(..., ge=0, description="Number of bedrooms available in the unit.")
    bathrooms: int = Field(..., ge=0, description="Number of bathrooms available in the unit.")
    amenities: List[str] = Field(default_factory=list, description="List of included amenities.")


class PredictionRequest(BaseModel):
    """Wrapper model exposing property details to the prediction endpoint."""

    property: PropertyFeatures = Field(..., description="All features describing the property.")


class PredictionResponse(BaseModel):
    """Model returned by the API with an estimated monthly rent."""

    suggested_price: float = Field(..., description="Estimated monthly rent in Bhutanese Ngultrum.")
    currency: str = Field(default="BTN", description="ISO 4217 currency code of the amount.")
    model_version: Optional[str] = Field(
        default=None, description="Version string of the model that produced the prediction."
    )
