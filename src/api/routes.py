"""API routers that expose prediction functionality."""
from fastapi import APIRouter, Depends, HTTPException

from src.core.config import Settings, get_settings
from src.schemas.prediction import PredictionRequest, PredictionResponse
from src.services.predictor import predictor

router = APIRouter()


@router.get("/", summary="Health check")
def read_root(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    """Basic endpoint to confirm the service is reachable."""

    return {"message": f"{settings.project_name} is running 🚀"}


@router.post("/predict", response_model=PredictionResponse, summary="Predict rental price")
def predict_price(
    payload: PredictionRequest, settings: Settings = Depends(get_settings)
) -> PredictionResponse:
    """Return a rental price suggestion for the supplied property."""

    features = payload.property
    try:
        estimate = predictor.predict(
            location=features.location,
            property_type=features.property_type,
            size_sqft=features.size_sqft,
            bedrooms=features.bedrooms,
            bathrooms=features.bathrooms,
            amenities_count=len(features.amenities),
            location_score=features.location_score,
        )
    except FileNotFoundError as exc:  # pragma: no cover - defensive guard
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return PredictionResponse(
        suggested_price=round(estimate, 2),
        currency="BTN",
        model_version=settings.model_version,
    )
