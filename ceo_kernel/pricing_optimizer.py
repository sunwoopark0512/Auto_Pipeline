"""Simple pricing optimization utilities."""

def optimize_pricing(mrr_goal: float, churn_rate: float, cac: float, arpu: float) -> None:
    lifetime_value = arpu / churn_rate
    target_cac = lifetime_value * 0.3
    print(f"Recommended ARPU: {arpu}, Target CAC: {target_cac}, LTV: {lifetime_value}")

if __name__ == "__main__":
    optimize_pricing(mrr_goal=1000, churn_rate=0.05, cac=100, arpu=50)
