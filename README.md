# SmartRent Bhutan – AI Powered Rental Price Prediction

SmartRent Bhutan is an AI-first platform that aims to provide fair and transparent
rental price recommendations across Bhutan. The project combines a FastAPI backend,
structured data schemas, and an extensible machine-learning pipeline to deliver
reliable pricing guidance based on location, building type, size, and amenities.

## Project Structure

```
src/
├── api/                # FastAPI routers and endpoint definitions
├── core/               # Configuration and application settings
├── schemas/            # Pydantic models shared across the service
├── services/           # Business logic such as prediction services
├── training/           # Placeholder ML training pipeline
└── main.py             # FastAPI application entry point

tests/                  # Automated test suite
```

## Getting Started

1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the FastAPI development server:
   ```bash
   uvicorn src.main:app --reload
   ```
3. Explore the interactive docs at `http://localhost:8000/docs`.

## API Overview

- `GET /` – Health check endpoint returning a simple status message.
- `POST /predict` – Accepts property features and returns a rental price suggestion
  in Bhutanese Ngultrum (BTN).

## Testing

Run the automated tests with:

```bash
pytest
```

## Model Training Scaffold

The `src/training/pipeline.py` module outlines the future machine-learning workflow,
including data loading, preprocessing, training, and persistence. Replace the
placeholder logic with your actual dataset and model training code as data becomes
available.
