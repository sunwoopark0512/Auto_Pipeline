from pe_kernel.post_merge_cloner import clone_and_merge


def test_clone_and_merge():
    spec = {"features": ["A"], "customers": 100}
    new_spec = clone_and_merge(spec, 200)
    assert new_spec["features"] == ["A", "Unified Billing Layer"]
    assert new_spec["customers"] == 200
    # original should remain unchanged
    assert spec["features"] == ["A"]
