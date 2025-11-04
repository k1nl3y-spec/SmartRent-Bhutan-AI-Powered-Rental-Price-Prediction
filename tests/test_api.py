"""Tests for the FastAPI application."""
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()
    assert "message" in payload


def test_prediction_endpoint() -> None:
    payload = {
        "property": {
            "location": "Thimphu",
            "location_score": 4.5,
            "property_type": "apartment",
            "size_sqft": 900,
            "bedrooms": 2,
            "bathrooms": 2,
            "amenities": ["parking", "balcony"],
        }
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["currency"] == "BTN"
    assert body["suggested_price"] > 0
