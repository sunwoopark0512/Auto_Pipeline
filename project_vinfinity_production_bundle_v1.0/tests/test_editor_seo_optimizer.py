from editor_seo_optimizer import optimize_text


def test_optimize_text():
    text = optimize_text("hello")
    assert text.endswith("[optimized]")
