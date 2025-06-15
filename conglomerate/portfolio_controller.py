import numpy as np


def allocate_growth_budget(global_portfolio, total_capex):
    weights = np.array([p["growth_potential"] for p in global_portfolio], dtype=float)
    weights /= weights.sum()
    allocation = weights * total_capex
    return allocation
