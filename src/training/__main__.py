"""CLI entry point for training the rental price model."""
from __future__ import annotations

from pathlib import Path

from src.training.pipeline import run_pipeline


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    data_path = project_root / "data" / "rental_listings.csv"
    model_output = project_root / "models" / "rental_price_model.joblib"
    result = run_pipeline(data_path=data_path, model_output=model_output)
    print("Model trained and saved to", result.model_path)
    print("Metrics:", result.metrics)


if __name__ == "__main__":
    main()
