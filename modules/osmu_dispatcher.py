from modules.osmu_content_slicer import slice_text
from modules.osmu_caption_generator import generate_caption
from modules.osmu_format_mapper import get_limits
from modules.hook_uploader import upload_to_wordpress  # 예시: 재활용
from modules.slack_notifier import send_slack_message
from utils.init_env import load_env

env = load_env()

def dispatch_to_platforms(title: str, full_text: str, slug: str, token: str):
    """
    1) 원문 슬라이스
    2) 플랫폼별 캡션·포맷 적용
    3) 업로드 훅 실행 (현재 예시: WordPress + Slack 알림)
       → 필요 시 YouTube/TikTok API 모듈을 추가해 확장
    """
    # 0. 공통 업로드(WordPress) — 이미 super_orchestrator에서 수행 가능
    upload_to_wordpress(title, full_text, slug, token)

    # 1. 추가 플랫폼 예시
    for plat in ["instagram", "twitter", "linkedin"]:
        limits = get_limits(plat)
        pieces = slice_text(full_text, limits["max_text"])
        caption = generate_caption(plat, pieces[0])

        # -- 실제 업로드 API 자리 --
        print(f"▶︎ [{plat}] upload: «{title}» ({len(pieces)} slice)")

        # Slack log
        send_slack_message(env["SLACK_WEBHOOK"],
                           f"📤 {plat.capitalize()} post queued: {title}")

    return True
