"""Pipeline 테스트."""

from codex.pipeline import Pipeline


def test_pipeline_creation():
    """파이프라인 생성 테스트."""
    pipeline = Pipeline()
    assert pipeline.steps == []


def test_add_step():
    """스텝 추가 테스트."""
    pipeline = Pipeline()
    pipeline.add_step("test", "echo", {"message": "Hello"})
    assert len(pipeline.steps) == 1
    assert pipeline.steps[0]["name"] == "test"
    assert pipeline.steps[0]["action"] == "echo"
    assert pipeline.steps[0]["params"] == {"message": "Hello"}


def test_run_pipeline():
    """파이프라인 실행 테스트."""
    pipeline = Pipeline()
    pipeline.add_step("test1", "echo", {"message": "Hello"})
    pipeline.add_step("test2", "echo", {"message": "World"})

    results = pipeline.run()
    assert len(results) == 2
    assert all(result["status"] == "success" for result in results)
