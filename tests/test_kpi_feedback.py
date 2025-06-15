from analytics.kpi_feedback import generate_feedback


def test_feedback_generation():
    kpi = {
        "click_through_rate": 7.8,
        "engagement_rate": 4.5,
        "watch_time": 15,
        "conversion_rate": 1.2,
    }
    fb = generate_feedback(kpi)
    assert fb["needed"] is True
    joined = " ".join(fb["feedback"])
    assert "썸네일" in joined
