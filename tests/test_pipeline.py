"""Pipeline 테스트."""

from typing import Dict

import pytest

from codex.pipeline import Pipeline, PipelineStep


@pytest.fixture
def sample_step_params() -> Dict[str, str]:
    """테스트용 스텝 파라미터."""
    return {"message": "Hello"}


def test_pipeline_creation() -> None:
    """파이프라인 생성 테스트."""
    pipeline = Pipeline()
    assert isinstance(pipeline.steps, list)
    assert len(pipeline.steps) == 0


def test_add_step(sample_step_params: Dict[str, str]) -> None:
    """스텝 추가 테스트."""
    pipeline = Pipeline()
    pipeline.add_step("test", "echo", sample_step_params)

    assert len(pipeline.steps) == 1
    assert isinstance(pipeline.steps[0], PipelineStep)
    assert pipeline.steps[0].name == "test"
    assert pipeline.steps[0].action == "echo"
    assert pipeline.steps[0].params == sample_step_params


def test_run_pipeline(sample_step_params: Dict[str, str]) -> None:
    """파이프라인 실행 테스트."""
    pipeline = Pipeline()
    pipeline.add_step("test1", "echo", sample_step_params)
    pipeline.add_step("test2", "echo", {"message": "World"})

    results = pipeline.run()
    assert len(results) == 2
    assert all(result["status"] == "success" for result in results)
