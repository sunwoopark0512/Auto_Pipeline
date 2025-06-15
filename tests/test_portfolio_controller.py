import numpy as np
from conglomerate.portfolio_controller import allocate_growth_budget


def test_allocate_growth_budget_basic():
    portfolio = [
        {"growth_potential": 1},
        {"growth_potential": 1},
    ]
    result = allocate_growth_budget(portfolio, 100)
    assert np.allclose(result, [50, 50])
