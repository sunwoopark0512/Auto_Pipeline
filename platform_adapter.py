#!/usr/bin/env python3
"""
platform_adapter.py
플랫폼별 알고리즘 정책 자동 대응 모듈
- 영상 길이, 자막 유무, 썸네일, 해시태그, CTA 자동 최적화
- TikTok / YouTube Shorts / Instagram Reels 대응
"""

from typing import Dict

PLATFORM_POLICIES = {
    "youtube_shorts": {
        "max_duration_sec": 60,
        "resolution": "1080x1920",
        "caption_required": True,
        "hashtags": ["#shorts", "#AI추천", "#오늘의정보"],
        "cta": "댓글로 당신의 생각을 남겨주세요!",
        "best_post_time": "17:00~20:00 (목/금/토)"
    },
    "tiktok": {
        "max_duration_sec": 90,
        "resolution": "1080x1920",
        "caption_required": True,
        "hashtags": ["#fyp", "#ai", "#funfacts"],
        "cta": "지금 저장하고 친구에게 공유하세요!",
        "best_post_time": "19:00~22:00 (화/수/토)"
    },
    "instagram_reels": {
        "max_duration_sec": 90,
        "resolution": "1080x1920",
        "caption_required": True,
        "hashtags": ["#reels", "#trend", "#mustsee"],
        "cta": "스토리로 공유하면 더 많은 친구들이 봐요!",
        "best_post_time": "18:00~21:00 (수/목/일)"
    }
}

def adapt_for_platform(platform: str, base_script: str) -> Dict:
    """플랫폼별 업로드 조건에 맞는 최적화 결과 반환"""
    policy = PLATFORM_POLICIES.get(platform)
    if not policy:
        raise ValueError(f"Unsupported platform: {platform}")

    final_script = f"{base_script.strip()}\n\n{policy['cta']}"
    return {
        "platform": platform,
        "script": final_script,
        "hashtags": policy["hashtags"],
        "caption_required": policy["caption_required"],
        "max_duration_sec": policy["max_duration_sec"],
        "post_time_recommendation": policy["best_post_time"]
    }

def print_policy_summary(platform: str):
    """플랫폼 정책 요약 출력"""
    policy = PLATFORM_POLICIES.get(platform)
    if not policy:
        print("❌ 해당 플랫폼 정책 없음")
        return
    print(f"📱 [{platform.upper()}] 알고리즘 최적화 가이드")
    for k, v in policy.items():
        print(f"  - {k}: {v}")

if __name__ == "__main__":
    platform = "tiktok"
    script = "요즘 사람들이 가장 많이 검색한 여행지는 어디일까요?"
    adapted = adapt_for_platform(platform, script)
    print_policy_summary(platform)
    print("\n📜 최종 스크립트 + CTA:\n", adapted["script"])
