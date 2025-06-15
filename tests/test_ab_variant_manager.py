"""A/B 테스트 변형 관리자 테스트."""

from datetime import datetime, timedelta

import pytest

from ab_variant_manager import ABVariantManager, Experiment, Variant


@pytest.fixture
def sample_variants():
    """테스트용 변형 샘플을 생성합니다."""
    return [
        Variant(
            id="v1", name="Control", weight=0.5, parameters={"feature_enabled": False}
        ),
        Variant(
            id="v2", name="Treatment", weight=0.5, parameters={"feature_enabled": True}
        ),
    ]


@pytest.fixture
def sample_experiment(sample_variants):
    """테스트용 실험 샘플을 생성합니다."""
    return Experiment(
        id="test_exp",
        name="Test Experiment",
        description="A test experiment",
        variants=sample_variants,
        start_date=datetime.utcnow() - timedelta(days=1),
        end_date=datetime.utcnow() + timedelta(days=30),
    )


def test_variant_validation():
    """변형 유효성 검사를 테스트합니다."""
    valid_variant = Variant(id="v1", name="Test", weight=0.5, parameters={})
    assert valid_variant.validate()

    invalid_variant = Variant(
        id="", name="Test", weight=1.5, parameters={}  # 유효하지 않은 가중치
    )
    assert not invalid_variant.validate()


def test_experiment_validation(sample_variants):
    """실험 유효성 검사를 테스트합니다."""
    valid_experiment = Experiment(
        id="exp1",
        name="Test",
        description="Test experiment",
        variants=sample_variants,
        start_date=datetime.utcnow(),
    )
    assert valid_experiment.validate()

    # 가중치 합이 1이 아닌 경우
    invalid_variants = [
        Variant(id="v1", name="A", weight=0.7, parameters={}),
        Variant(id="v2", name="B", weight=0.7, parameters={}),
    ]
    invalid_experiment = Experiment(
        id="exp2",
        name="Test",
        description="Invalid experiment",
        variants=invalid_variants,
        start_date=datetime.utcnow(),
    )
    assert not invalid_experiment.validate()


def test_add_experiment(sample_experiment):
    """실험 추가를 테스트합니다."""
    manager = ABVariantManager()
    manager.add_experiment(sample_experiment)
    assert sample_experiment.id in manager.experiments

    with pytest.raises(ValueError):
        manager.add_experiment(sample_experiment)  # 중복 ID


def test_get_variant(sample_experiment):
    """변형 선택을 테스트합니다."""
    manager = ABVariantManager()
    manager.add_experiment(sample_experiment)

    # 같은 사용자는 항상 같은 변형을 받아야 함
    user_id = "test_user"
    variant1 = manager.get_variant(sample_experiment.id, user_id)
    variant2 = manager.get_variant(sample_experiment.id, user_id)
    assert variant1 == variant2

    # 다른 사용자는 다른 변형을 받을 수 있음
    other_variant = manager.get_variant(sample_experiment.id, "other_user")
    # Note: 이론적으로는 같은 변형이 선택될 수 있으나 확률은 낮음


def test_experiment_timing():
    """실험 타이밍을 테스트합니다."""
    future_experiment = Experiment(
        id="future",
        name="Future Test",
        description="Future experiment",
        variants=[Variant(id="v1", name="A", weight=1.0, parameters={})],
        start_date=datetime.utcnow() + timedelta(days=1),
    )

    manager = ABVariantManager()
    manager.add_experiment(future_experiment)

    # 시작 전에는 변형을 받지 않아야 함
    assert manager.get_variant(future_experiment.id, "user1") is None


def test_track_event(sample_experiment):
    """이벤트 추적을 테스트합니다."""
    manager = ABVariantManager()
    manager.add_experiment(sample_experiment)

    # 이벤트 추적이 오류 없이 실행되어야 함
    manager.track_event(
        sample_experiment.id, "test_user", "page_view", {"page": "home"}
    )

    # 존재하지 않는 실험에 대한 이벤트 추적
    with pytest.raises(ValueError):
        manager.track_event("nonexistent", "test_user", "page_view")
