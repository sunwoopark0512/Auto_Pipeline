"""Portfolio allocation utilities."""

import numpy as np

def optimize_allocation(portfolio: list[dict], max_budget: float) -> np.ndarray:
    """Allocate budget inversely proportional to risk."""
    weights = np.array([1 / p["risk"] for p in portfolio], dtype=float)
    weights /= weights.sum()
    allocation = weights * max_budget
    return allocation
