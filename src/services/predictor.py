"""Service layer responsible for computing rental price predictions."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass
class BaselinePredictor:
    """A lightweight rule-based predictor used until an ML model is trained."""

    base_rate: float = 5000.0
    location_weight: float = 1000.0
    size_weight: float = 150.0
    amenity_weight: float = 250.0

    def predict(self, *, location_score: float, size_sqft: float, amenities: Iterable[str]) -> float:
        """Return a naive rental price estimate.

        The heuristic treats the location as a multiplier, adds a contribution from
        the floor area, and a bonus for every amenity supplied.
        """

        amenity_bonus = len(list(amenities)) * self.amenity_weight
        return (
            self.base_rate
            + (location_score * self.location_weight)
            + (size_sqft * self.size_weight)
            + amenity_bonus
        )


predictor = BaselinePredictor()
