import numpy as np
from pe_kernel.portfolio_optimizer import optimize_allocation


def test_optimize_allocation():
    portfolio = [{"risk": 1}, {"risk": 2}]
    allocation = optimize_allocation(portfolio, 100)
    weights = np.array([1 / 1, 1 / 2], dtype=float)
    weights /= weights.sum()
    expected = weights * 100
    assert np.allclose(allocation, expected)
