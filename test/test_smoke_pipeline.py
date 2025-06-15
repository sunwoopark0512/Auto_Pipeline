from run_pipeline import run_pipeline


def test_pipeline():
    assert callable(run_pipeline)
    run_pipeline()
