"""Basic SaaS valuation utilities."""

def valuate(mrr: float, growth: float, churn: float, margin: float) -> float:
    """Return estimated value using a simple LTV multiple."""
    ltv = (mrr * (1 + growth - churn)) * 12
    value = ltv * margin * 5
    return value
