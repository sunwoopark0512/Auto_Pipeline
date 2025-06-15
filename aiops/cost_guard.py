import boto3
from datetime import datetime


def gpu_cost_forecast(budget: float) -> bool:
    """Return True if forecasted GPU usage is within budget."""
    ce = boto3.client("ce")
    now = datetime.utcnow().strftime("%Y-%m-%d")
    res = ce.get_cost_forecast(
        TimePeriod={"Start": now, "End": now},
        Granularity="DAILY",
        Metric="UsageQuantity",
        PredictionIntervalLevel=95,
    )
    forecast = float(res["ForecastResultsByTime"][0]["MeanValue"])
    return forecast < budget


if __name__ == "__main__":
    if not gpu_cost_forecast(2000):
        raise RuntimeError("Budget forecast exceeded for GPU training")
