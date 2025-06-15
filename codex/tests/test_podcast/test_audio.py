"""팟캐스트 오디오 처리 테스트."""

from pathlib import Path

import pytest
from pydub import AudioSegment

from podcast.audio import AudioProcessor


@pytest.fixture
def temp_dir(tmp_path):
    """임시 디렉토리를 생성합니다."""
    return tmp_path


@pytest.fixture
def sample_audio(temp_dir):
    """샘플 오디오 파일을 생성합니다."""
    sample_path = temp_dir / "sample.mp3"
    audio = AudioSegment.silent(duration=1000)  # 1초 무음
    audio.export(str(sample_path), format="mp3")
    return sample_path


@pytest.fixture
def processor(temp_dir):
    """오디오 처리기 인스턴스를 생성합니다."""
    return AudioProcessor(temp_dir / "output")


def test_convert_to_mp3(processor, sample_audio):
    """MP3 변환을 테스트합니다."""
    output_path = processor.convert_to_mp3(sample_audio)
    assert output_path.exists()
    assert output_path.suffix == ".mp3"


def test_get_duration(processor, sample_audio):
    """재생 시간 측정을 테스트합니다."""
    duration = processor.get_duration(sample_audio)
    assert duration is not None
    assert duration > 0


def test_normalize_audio(processor, sample_audio):
    """오디오 정규화를 테스트합니다."""
    output_path = processor.normalize_audio(sample_audio)
    assert output_path.exists()
    assert output_path.suffix == ".mp3"


def test_invalid_input(processor):
    """잘못된 입력 처리를 테스트합니다."""
    with pytest.raises(ValueError):
        processor.convert_to_mp3(Path("nonexistent.mp3"))

    with pytest.raises(ValueError):
        processor.normalize_audio(Path("nonexistent.mp3"))
