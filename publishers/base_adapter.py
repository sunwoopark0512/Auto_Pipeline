import os
from abc import ABC, abstractmethod

def is_dryrun() -> bool:
    return os.getenv("DRYRUN", "false").lower() == "true"

class PublisherAdapter(ABC):
    """공통 인터페이스 + DRY-RUN 지원"""

    @abstractmethod
    def _real_publish(self, content: dict) -> str:
        """실제 API 호출 (서브클래스 구현)"""

    def publish(self, content: dict) -> str:
        if is_dryrun():
            print(f"\N{CLOCKWISE OPEN CIRCLE ARROW} DRY-RUN: {self.__class__.__name__} 업로드 생략")
            return "DRYRUN_URL"
        return self._real_publish(content)
