#!/usr/bin/env python3
"""
video_generator.py
스크립트 기반 숏폼/롱폼 영상 자동 생성기
- TTS (음성 합성) → 음성 파일 생성
- BGM 및 텍스트 오버레이 추가
- 영상 출력 (FFmpeg 사용)
"""

import os
import uuid
from gtts import gTTS
from moviepy import (
    AudioFileClip,
    CompositeVideoClip,
    TextClip,
    VideoFileClip,
)

# pylint: disable=no-member


def text_to_speech(
    text: str,
    lang: str = "ko",
    output_dir: str = "outputs/audio",
) -> str:
    """스크립트를 TTS로 변환하여 mp3 저장"""
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(output_dir, filename)
    tts = gTTS(text=text, lang=lang)
    tts.save(filepath)
    return filepath


def create_video_with_audio(
    script_text: str,
    bg_video_path: str = "assets/bg_default.mp4",
    output_path: str = "outputs/final_video.mp4",
) -> None:
    """TTS 오디오 + 배경 영상 + 텍스트 오버레이로 숏폼 영상 생성"""
    os.makedirs("outputs", exist_ok=True)

    # TTS
    audio_path = text_to_speech(script_text)

    # 배경 영상 클립
    video_clip = (
        VideoFileClip(bg_video_path)
        .subclip(0, 15)
        .resize(height=1920, width=1080)
    )

    # TTS 오디오
    audio_clip = AudioFileClip(audio_path)
    video_clip = video_clip.set_audio(audio_clip)

    # 텍스트 오버레이
    txt_clip = TextClip(
        script_text,
        fontsize=60,
        color="white",
        bg_color="black",
        size=video_clip.size,
        method="caption",
    )
    txt_clip = txt_clip.set_duration(audio_clip.duration).set_position(
        "center"
    )

    # 최종 영상 합성
    final = CompositeVideoClip([video_clip, txt_clip])
    final = final.set_duration(audio_clip.duration)

    # 저장
    final.write_videofile(output_path, fps=24)
    print(f"✅ 영상 생성 완료: {output_path}")


if __name__ == "__main__":
    SCRIPT = (
        "지금 당장 떠나야 할 최고의 여행지, "
        "몰타를 소개합니다. 유럽과 지중해가 만나는 그곳!"
    )
    create_video_with_audio(SCRIPT)
