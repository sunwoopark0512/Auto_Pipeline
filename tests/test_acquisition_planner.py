from pe_kernel.acquisition_planner import plan_acquisition


def test_plan_acquisition():
    plan = plan_acquisition(100000, 0.3)
    assert plan["offer_price"] == 100000
    assert plan["post_merge_budget"] == 60000
    assert plan["team_expansion"] == 3
