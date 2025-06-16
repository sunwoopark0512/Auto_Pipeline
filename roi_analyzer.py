import json


def load_specs(path):
    """Load channel specifications from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_roi(spec):
    """Compute ROI for a single channel spec.

    ROI is defined as (revenue - cost) / cost. If cost is zero, return
    infinity when revenue is positive, otherwise 0.
    """
    cost = spec.get("cost", 0)
    revenue = spec.get("revenue", 0)
    if cost == 0:
        return float("inf") if revenue > 0 else 0
    return (revenue - cost) / cost


def rank_channels(specs):
    """Rank channels by ROI in descending order.

    Returns a new list of specs including the computed ROI for each
    channel, sorted from highest ROI to lowest.
    """
    specs_with_roi = []
    for spec in specs:
        roi = compute_roi(spec)
        item = spec.copy()
        item["roi"] = roi
        specs_with_roi.append(item)
    return sorted(specs_with_roi, key=lambda x: x["roi"], reverse=True)
