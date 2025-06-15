"""Adaptive GPU allocation based on spot price."""
from __future__ import annotations

import boto3  # type: ignore[import-untyped]


def current_spot_price(instance_type: str = "p4d.24xlarge") -> float:
    """Return latest spot price for the given instance type."""
    ec2 = boto3.client("ec2")
    history = ec2.describe_spot_price_history(
        InstanceTypes=[instance_type],
        ProductDescriptions=["Linux/UNIX"],
        MaxResults=1,
    )
    return float(history["SpotPriceHistory"][0]["SpotPrice"])


def allocate_gpu(price_threshold: float = 6.0) -> str:
    """Allocate GPU resources depending on spot price."""
    price = current_spot_price()
    if price > price_threshold:
        msg = "High spot price, switching to on-demand reservation"
        print(msg)
        # Placeholder for on-demand allocation logic
        return "on-demand"
    msg = "Spot price acceptable, allocating spot fleet"
    print(msg)
    return "spot"


if __name__ == "__main__":
    allocate_gpu()
