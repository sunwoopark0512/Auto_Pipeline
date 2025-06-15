"""Simple acquisition planning utilities."""

def plan_acquisition(value: float, growth_plan: float) -> dict:
    """Return a basic acquisition plan dictionary."""
    invest_budget = value * 0.6
    hiring_plan = int(growth_plan * 10)
    return {
        "offer_price": value,
        "post_merge_budget": invest_budget,
        "team_expansion": hiring_plan,
    }
