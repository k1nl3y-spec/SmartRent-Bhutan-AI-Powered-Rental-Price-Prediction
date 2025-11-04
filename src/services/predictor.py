"""Service layer responsible for computing rental price predictions."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import joblib
import pandas as pd

from src.core.config import get_settings
from src.training.pipeline import run_pipeline


@dataclass
class RentalPricePredictor:
    """Wrapper around a persisted sklearn pipeline used for inference."""

    model_path: Path
    training_data_path: Path
    auto_train: bool = True
    _model: Optional[object] = field(default=None, init=False, repr=False)

    def _ensure_model_file(self) -> None:
        """Create the trained model artefact if it does not already exist."""

        if self.model_path.exists():
            return
        if not self.auto_train:
            raise FileNotFoundError(
                f"Trained model not found at {self.model_path}. Run the training pipeline first."
            )
        run_pipeline(data_path=self.training_data_path, model_output=self.model_path)

    def load(self) -> None:
        """Load the trained pipeline from disk if it is not already available."""

        if self._model is None:
            self._ensure_model_file()
            self._model = joblib.load(self.model_path)

    def predict(
        self,
        *,
        location: str,
        property_type: str,
        size_sqft: float,
        bedrooms: int,
        bathrooms: int,
        amenities_count: int,
        location_score: float,
    ) -> float:
        """Return the rental price prediction for the supplied features."""

        self.load()
        assert self._model is not None  # for mypy/static checkers
        features = pd.DataFrame(
            [
                {
                    "location": location,
                    "property_type": property_type,
                    "size_sqft": size_sqft,
                    "bedrooms": bedrooms,
                    "bathrooms": bathrooms,
                    "amenities_count": amenities_count,
                    "location_score": location_score,
                }
            ]
        )
        prediction = self._model.predict(features)[0]
        return float(prediction)


BASE_DIR = Path(__file__).resolve().parents[2]
SETTINGS = get_settings()
MODEL_PATH = (BASE_DIR / SETTINGS.model_path).resolve()
TRAINING_DATA_PATH = (BASE_DIR / SETTINGS.training_data_path).resolve()

predictor = RentalPricePredictor(
    model_path=MODEL_PATH,
    training_data_path=TRAINING_DATA_PATH,
)
