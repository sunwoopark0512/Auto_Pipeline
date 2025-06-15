"""Podcast 오디오 처리 모듈."""

from pathlib import Path
from typing import Optional

from mutagen import File as MutagenFile
from pydub import AudioSegment


class AudioProcessor:
    """팟캐스트 오디오 처리기."""

    def __init__(self, output_dir: Path) -> None:
        """오디오 처리기를 초기화합니다.

        Args:
            output_dir: 출력 디렉토리 경로
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def convert_to_mp3(
        self,
        input_path: Path,
        bitrate: str = "192k",
        sample_rate: int = 44100,
    ) -> Path:
        """오디오를 MP3 형식으로 변환합니다.

        Args:
            input_path: 입력 파일 경로
            bitrate: 출력 비트레이트
            sample_rate: 출력 샘플레이트

        Returns:
            Path: 변환된 MP3 파일 경로

        Raises:
            ValueError: 입력 파일이 존재하지 않는 경우
        """
        if not input_path.exists():
            raise ValueError(f"Input file not found: {input_path}")

        audio = AudioSegment.from_file(str(input_path))
        audio = audio.set_frame_rate(sample_rate)

        output_path = self.output_dir / f"{input_path.stem}_converted.mp3"
        audio.export(str(output_path), format="mp3", bitrate=bitrate)

        return output_path

    def get_duration(self, file_path: Path) -> Optional[float]:
        """오디오 파일의 재생 시간을 초 단위로 반환합니다."""
        try:
            audio = MutagenFile(str(file_path))
            if audio and hasattr(audio.info, "length"):
                return float(audio.info.length)
        except Exception:
            pass
        return None

    def normalize_audio(self, input_path: Path, target_db: float = -20.0) -> Path:
        """오디오 레벨을 정규화합니다."""
        if not input_path.exists():
            raise ValueError(f"Input file not found: {input_path}")

        audio = AudioSegment.from_file(str(input_path))
        change_in_db = target_db - audio.dBFS
        normalized_audio = audio.apply_gain(change_in_db)

        output_path = self.output_dir / f"{input_path.stem}_normalized.mp3"
        normalized_audio.export(str(output_path), format="mp3")

        return output_path
