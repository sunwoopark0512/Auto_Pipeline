"""
파이프라인 단계 정의.
각 이름은 import 가능한 모듈이어야 하며, 모듈 안에 `main()` 함수가 존재해야 합니다.
"""

PIPELINE_ORDER = [
    "cursor_chunk_doc_gen",
    "auto_rewriter",
    "qa_tester",
    "auto_insight",
    "hook_uploader",
]

# 모든 단계 완료 후 항상 실행할 알림/후처리 스텝 (선택)
# 모듈에 `main(failures: list[str])` 시그니처 필요
NOTIFIER_STEP = "retry_dashboard_notifier"
