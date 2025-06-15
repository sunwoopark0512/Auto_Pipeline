"""Utilities for cloning and merging SaaS specs."""

def clone_and_merge(original_spec: dict, target_customers: int) -> dict:
    """Return a new spec with unified billing and updated customers."""
    new_spec = original_spec.copy()
    # ensure features list is copied to avoid mutating original
    features = list(original_spec.get("features", []))
    features.append("Unified Billing Layer")
    new_spec["features"] = features
    new_spec["customers"] = target_customers
    return new_spec
