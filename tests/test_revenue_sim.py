import os, sys; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.revenue_sim import simulate, Params


def test_simulate_one_month():
    result = simulate(Params(months=1))
    assert result[0]["month"] == 1
    assert result[0]["active"] > 0
    assert result[0]["mrr"] == result[0]["active"] * Params().price
