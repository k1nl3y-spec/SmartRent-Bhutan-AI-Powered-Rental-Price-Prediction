"""Training pipeline for rental price prediction models."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


@dataclass
class PipelineResult:
    """Container describing the outcome of a training run."""

    model_path: Path
    metrics: Dict[str, float]


class TrainingPipeline:
    """End-to-end workflow for fitting and persisting a rental price model."""

    def __init__(
        self,
        data_path: Path,
        model_output: Path,
        *,
        target_column: str = "rent",
        test_size: float = 0.2,
        random_state: int = 42,
    ) -> None:
        self.data_path = data_path
        self.model_output = model_output
        self.target_column = target_column
        self.test_size = test_size
        self.random_state = random_state

    def load_data(self) -> pd.DataFrame:
        """Load raw rental data from disk."""

        if not self.data_path.exists():
            raise FileNotFoundError(f"Training data not found at {self.data_path}")
        data = pd.read_csv(self.data_path)
        if data.empty:
            raise ValueError("Training dataset is empty; cannot train model")
        missing_columns = {self.target_column} - set(data.columns)
        if missing_columns:
            raise ValueError(
                f"Dataset is missing required column(s): {', '.join(sorted(missing_columns))}"
            )
        return data

    def split_features(self, data: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
        """Separate features from the target column."""

        features = data.drop(columns=[self.target_column])
        target = data[self.target_column]
        return features, target

    def build_pipeline(self, features: pd.DataFrame) -> Pipeline:
        """Construct the preprocessing + model pipeline."""

        categorical_features = ["location", "property_type"]
        numeric_features = [
            "size_sqft",
            "bedrooms",
            "bathrooms",
            "amenities_count",
            "location_score",
        ]

        for column in categorical_features + numeric_features:
            if column not in features.columns:
                raise ValueError(f"Required feature column '{column}' missing from dataset")

        categorical_transformer = OneHotEncoder(handle_unknown="ignore")
        numeric_transformer = Pipeline(
            steps=[("scaler", StandardScaler(with_mean=False))]
        )

        preprocessor = ColumnTransformer(
            transformers=[
                ("categorical", categorical_transformer, categorical_features),
                ("numeric", numeric_transformer, numeric_features),
            ]
        )

        model = RandomForestRegressor(
            n_estimators=200,
            random_state=self.random_state,
            n_jobs=-1,
        )

        return Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])

    def train(self, pipeline: Pipeline, features: pd.DataFrame, target: pd.Series) -> Pipeline:
        """Fit the pipeline on the provided features and target."""

        pipeline.fit(features, target)
        return pipeline

    def evaluate(
        self, pipeline: Pipeline, features: pd.DataFrame, target: pd.Series
    ) -> Dict[str, float]:
        """Generate evaluation metrics on holdout data."""

        predictions = pipeline.predict(features)
        return {
            "mae": float(mean_absolute_error(target, predictions)),
            "r2": float(r2_score(target, predictions)),
        }

    def persist(self, pipeline: Pipeline) -> Path:
        """Persist the trained pipeline to disk."""

        self.model_output.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(pipeline, self.model_output)
        return self.model_output

    def run(self) -> PipelineResult:
        """Execute the full pipeline end-to-end and return metrics."""

        data = self.load_data()
        features, target = self.split_features(data)
        train_features, test_features, train_target, test_target = train_test_split(
            features,
            target,
            test_size=self.test_size,
            random_state=self.random_state,
        )
        pipeline = self.build_pipeline(train_features)
        trained_pipeline = self.train(pipeline, train_features, train_target)
        metrics = self.evaluate(trained_pipeline, test_features, test_target)
        model_path = self.persist(trained_pipeline)
        return PipelineResult(model_path=model_path, metrics=metrics)


def run_pipeline(data_path: Path, model_output: Path) -> PipelineResult:
    """Convenience function for scripts and notebooks."""

    return TrainingPipeline(data_path=data_path, model_output=model_output).run()
