import logging
import asyncio
from data_sources import (
    fetch_google_analytics,
    fetch_search_console,
    fetch_social_insights,
    fetch_email_marketing,
    fetch_industry_reports,
)
from feedback_loop import (
    analyze_comment_sentiment,
    monitor_social_mentions,
    analyze_user_behavior,
    apply_feedback,
)
from cross_platform_integrator import integrate_data

# ---------------------- 로깅 설정 ----------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- 전체 파이프라인 ----------------------

async def run_pipeline() -> None:
    logging.info("블로그 자동화 파이프라인 시작")

    # 1차 데이터 수집 병렬 실행
    ga_task = asyncio.create_task(fetch_google_analytics())
    sc_task = asyncio.create_task(fetch_search_console())
    social_task = asyncio.create_task(fetch_social_insights())
    email_task = asyncio.create_task(fetch_email_marketing())

    # 2차 데이터 수집
    industry_task = asyncio.create_task(fetch_industry_reports())

    ga, sc, social, email, industry = await asyncio.gather(
        ga_task, sc_task, social_task, email_task, industry_task
    )

    # 실시간 피드백 수집 병렬 실행
    comments_fb = asyncio.create_task(analyze_comment_sentiment([]))
    mentions_fb = asyncio.create_task(monitor_social_mentions("brand"))
    behavior_fb = asyncio.create_task(analyze_user_behavior(ga))

    feedback_results = await asyncio.gather(comments_fb, mentions_fb, behavior_fb)
    feedback = {k: v for result in feedback_results for k, v in result.items()}
    await apply_feedback(feedback)

    # 데이터 통합
    integrated = integrate_data(ga, sc, social, email, industry)
    logging.info(f"통합 결과: {integrated}")
    logging.info("파이프라인 종료")

if __name__ == "__main__":
    asyncio.run(run_pipeline())

