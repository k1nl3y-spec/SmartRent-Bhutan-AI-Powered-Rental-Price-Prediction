# SmartRent Bhutan – AI Powered Rental Price Prediction

SmartRent Bhutan is an AI-first platform that provides transparent rental price
recommendations across Bhutan. The project combines a FastAPI backend, typed
request/response schemas, and a reproducible machine-learning pipeline to
deliver reliable pricing guidance based on location, building type, size, and
amenities.

## Project Structure

```
src/
├── api/                # FastAPI routers and endpoint definitions
├── core/               # Configuration and application settings
├── schemas/            # Pydantic models shared across the service
├── services/           # Business logic such as prediction services
├── training/           # Model training pipeline and CLI entry point
└── main.py             # FastAPI application entry point

data/                   # Sample rental dataset used for training
models/                 # Persisted machine learning artefacts (generated)
tests/                  # Automated test suite
```

## Getting Started

1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Train the model artefact (first run only):
   ```bash
   python -m src.training
   ```
   The command trains a scikit-learn pipeline on the data in
   `data/rental_listings.csv` and stores the artefact at
   `models/rental_price_model.joblib`. The repository ignores generated model
   files, and the API will automatically invoke the training pipeline on first
   use if the artefact is missing.
3. Run the FastAPI development server:
   ```bash
   uvicorn src.main:app --reload
   ```
4. Explore the interactive docs at `http://localhost:8000/docs`.

## API Overview

- `GET /` – Health check endpoint returning a simple status message.
- `POST /predict` – Accepts property features and returns a rental price
  suggestion in Bhutanese Ngultrum (BTN) using the trained model.

The prediction endpoint expects payloads shaped like the example below:

```json
{
  "property": {
    "location": "Thimphu",
    "location_score": 4.5,
    "property_type": "apartment",
    "size_sqft": 900,
    "bedrooms": 3,
    "bathrooms": 2,
    "amenities": ["parking", "balcony"]
  }
}
```

## Model Training Pipeline

The pipeline located at `src/training/pipeline.py` orchestrates the full
workflow:

1. Load the dataset from `data/rental_listings.csv`.
2. Split the data into train/test sets.
3. Build a preprocessing and modelling pipeline that encodes categorical
   fields and scales numeric features before fitting a `RandomForestRegressor`.
4. Evaluate the trained model using R² and MAE metrics.
5. Persist the fitted pipeline to `models/rental_price_model.joblib` for use by
   the API.

Because the repository does not store binary artefacts, you should rerun the
training command whenever you change the dataset or model configuration. The
API also regenerates the artefact automatically if it is missing so local
development remains frictionless.

## Testing

Run the automated tests with:

```bash
pytest
```
