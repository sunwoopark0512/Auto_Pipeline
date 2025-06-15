"""
KPI 값을 받아 자동 피드백 메시지·액션 항목을 생성한다.

Usage:
    from analytics.kpi_feedback import generate_feedback
    feedback = generate_feedback(kpi_dict)
"""
from typing import Dict, List, Union

_BENCHMARKS = {
    "click_through_rate": 8.0,   # %
    "engagement_rate": 5.0,      # %
    "watch_time": 20,            # 분
    "conversion_rate": 2.0       # %
}


def _rate(value: float, target: float) -> str:
    """Return rating level compared to target."""
    if value >= target:
        return "good"
    if value >= target * 0.8:
        return "medium"
    return "poor"


def generate_feedback(kpi: Dict[str, float]) -> Dict[str, Union[List[str], bool]]:
    """Generate feedback actions for the given KPI values."""
    actions: List[str] = []
    for metric, target in _BENCHMARKS.items():
        val = kpi.get(metric, 0)
        rating = _rate(val, target)
        if rating == "good":
            continue
        if metric == "engagement_rate":
            actions.append("리텐션 강화를 위해 콘텐츠 길이·후킹 구간 재검토")
        elif metric == "click_through_rate":
            actions.append("썸네일·헤드라인 A/B 테스트 실행")
        elif metric == "watch_time":
            actions.append("초반 15초 내 몰입도 향상 요소 추가")
        elif metric == "conversion_rate":
            actions.append("CTA 위치·문구 최적화 및 랜딩페이지 속도 개선")
    return {"feedback": actions or ["모든 KPI 목표 충족"], "needed": bool(actions)}
