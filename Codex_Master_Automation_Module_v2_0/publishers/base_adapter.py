from abc import ABC, abstractmethod

class PublisherAdapter(ABC):
    """공통 퍼블리셔 어댑터 인터페이스."""

    @abstractmethod
    def publish(self, content: dict) -> str:
        """콘텐츠를 업로드하고 게시물 URL을 반환한다."""
        raise NotImplementedError
