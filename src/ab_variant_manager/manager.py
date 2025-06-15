"""A/B 테스트 변형 관리자 모듈."""

import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Variant:
    """A/B 테스트 변형 데이터 클래스."""

    id: str
    name: str
    weight: float
    parameters: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True

    def validate(self) -> bool:
        """변형의 유효성을 검사합니다.

        Returns:
            bool: 변형이 유효하면 True
        """
        return (
            bool(self.id)
            and bool(self.name)
            and 0.0 <= self.weight <= 1.0
            and isinstance(self.parameters, dict)
        )


@dataclass
class Experiment:
    """A/B 테스트 실험 데이터 클래스."""

    id: str
    name: str
    description: str
    variants: List[Variant]
    start_date: datetime
    end_date: Optional[datetime] = None
    is_active: bool = True

    def validate(self) -> bool:
        """실험의 유효성을 검사합니다.

        Returns:
            bool: 실험이 유효하면 True
        """
        return (
            bool(self.id)
            and bool(self.name)
            and bool(self.variants)
            and all(v.validate() for v in self.variants)
            and abs(sum(v.weight for v in self.variants) - 1.0) < 0.0001
        )


class ABVariantManager:
    """A/B 테스트 변형 관리자."""

    def __init__(self) -> None:
        """변형 관리자를 초기화합니다."""
        self.experiments: Dict[str, Experiment] = {}

    def add_experiment(self, experiment: Experiment) -> None:
        """새로운 실험을 추가합니다.

        Args:
            experiment: 추가할 실험

        Raises:
            ValueError: 실험이 유효하지 않은 경우
        """
        if not experiment.validate():
            raise ValueError("Invalid experiment configuration")

        if experiment.id in self.experiments:
            raise ValueError(f"Experiment with ID {experiment.id} already exists")

        self.experiments[experiment.id] = experiment

    def get_variant(self, experiment_id: str, user_id: str) -> Optional[Variant]:
        """사용자에 대한 변형을 가져옵니다.

        Args:
            experiment_id: 실험 ID
            user_id: 사용자 ID

        Returns:
            Optional[Variant]: 선택된 변형 또는 None

        Raises:
            ValueError: 실험이 존재하지 않는 경우
        """
        if experiment_id not in self.experiments:
            raise ValueError(f"Experiment {experiment_id} not found")

        experiment = self.experiments[experiment_id]
        if not experiment.is_active:
            return None

        now = datetime.utcnow()
        if experiment.end_date and now > experiment.end_date:
            experiment.is_active = False
            return None

        if now < experiment.start_date:
            return None

        # 사용자 ID를 기반으로 일관된 변형 선택
        random.seed(f"{experiment_id}:{user_id}")
        active_variants = [v for v in experiment.variants if v.is_active]
        if not active_variants:
            return None

        weights = [v.weight for v in active_variants]
        return random.choices(active_variants, weights=weights, k=1)[0]

    def track_event(
        self,
        experiment_id: str,
        user_id: str,
        event_type: str,
        event_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """실험 이벤트를 추적합니다.

        Args:
            experiment_id: 실험 ID
            user_id: 사용자 ID
            event_type: 이벤트 유형
            event_data: 이벤트 데이터

        Raises:
            ValueError: 실험이나 변형을 찾을 수 없는 경우
        """
        variant = self.get_variant(experiment_id, user_id)
        if not variant:
            return

        # 여기에 이벤트 추적 로직 구현
        # 예: 데이터베이스에 저장, 로그 시스템에 전송 등
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "experiment_id": experiment_id,
            "variant_id": variant.id,
            "user_id": user_id,
            "event_type": event_type,
            "event_data": event_data or {},
        }
        # print(f"Tracked event: {event}")  # 실제 구현에서는 적절한 저장/전송 로직으로 대체
