import os
import json
import logging
from datetime import datetime
from itertools import islice
from concurrent.futures import ThreadPoolExecutor, as_completed
from pytrends.request import TrendReq
import snscrape.modules.twitter as sntwitter
import requests
import random  # CPC 더미 데이터용

# ---------------------- 설정 ----------------------
CONFIG_PATH = os.getenv("TOPIC_CHANNELS_PATH", "config/topic_channels.json")
OUTPUT_PATH = os.getenv("KEYWORD_OUTPUT_PATH", "data/keyword_output_with_cpc.json")

GOOGLE_TRENDS_MIN_SCORE = 60
GOOGLE_TRENDS_MIN_GROWTH = 1.3
TWITTER_MIN_MENTIONS = 30
TWITTER_MIN_TOP_RETWEET = 50
MIN_CPC = 1000  # 원 (더미 기준)
YOUTUBE_MIN_AVG_VIEWS = 5000
INSTAGRAM_MIN_AVG_LIKES = 300
TIKTOK_MIN_AVG_VIEWS = 5000

# ---------------------- 로깅 설정 ----------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

# ---------------------- 토픽별 세부 키워드 쌍 ----------------------
TOPIC_DETAILS = {
    "여행": ["국내여행", "해외여행", "배낭여행"],
    "다이어트": ["간헐적단식", "홈트", "저탄고지"],
    "재테크": ["주식", "부동산", "가상화폐"],
    "뷰티": ["스킨케어", "메이크업", "헤어케어"],
    "건강": ["면역력", "운동", "영양제"],
    "AI": ["챗GPT", "머신러닝", "인공지능활용"],
    "취업": ["이력서작성", "면접팁", "직무역량"],
    "연애": ["소개팅", "데이트코스", "연애심리"],
    "자기계발": ["시간관리", "독서법", "습관형성"],
    "육아": ["영유아발달", "육아팁", "교육방법"]
}

# ---------------------- 키워드 쌍 생성 ----------------------
def generate_keyword_pairs(topic_details):
    pairs = []
    for topic, subs in topic_details.items():
        for sub in subs:
            pairs.append(f"{topic} {sub}")
    return pairs

# ---------------------- CPC 캐시 ----------------------
cpc_cache = {}

def fetch_cpc_dummy(keyword):
    if keyword not in cpc_cache:
        cpc_cache[keyword] = random.randint(500, 2000)
        logging.debug(f"CPC 캐시 생성: {keyword} = {cpc_cache[keyword]}")
    return cpc_cache[keyword]

# ---------------------- 데이터 수집 함수 ----------------------
def fetch_google_trends(keyword, pytrends):
    try:
        pytrends.build_payload([keyword], cat=0, timeframe='now 7-d', geo='KR')
        data = pytrends.interest_over_time()
        if data.empty or keyword not in data:
            logging.warning(f"Google Trends: '{keyword}' 데이터 없음")
            return None

        recent_avg = data[keyword][-3:].mean()
        past_avg = data[keyword][-7:].mean()
        growth = round(recent_avg / past_avg, 2) if past_avg > 0 else 0

        result = {
            "keyword": keyword,
            "source": "GoogleTrends",
            "score": int(recent_avg),
            "growth": growth,
            "cpc": fetch_cpc_dummy(keyword)
        }
        logging.info(f"Google Trends 수집 완료: {keyword} score={result['score']} growth={result['growth']} cpc={result['cpc']}")
        return result
    except Exception as e:
        logging.error(f"Google Trends 에러 '{keyword}': {e}")
        return None

def fetch_twitter_metrics(keyword, max_tweets=100):
    try:
        tweets_iter = sntwitter.TwitterSearchScraper(f'#{keyword} lang:ko').get_items()
        tweets = list(islice(tweets_iter, max_tweets))
        if not tweets:
            logging.warning(f"Twitter: '{keyword}' 트윗 없음")
            return None

        top_retweets = sorted((t.retweetCount for t in tweets), reverse=True)
        mentions = len(tweets)

        result = {
            "keyword": keyword,
            "source": "Twitter",
            "mentions": mentions,
            "top_retweet": top_retweets[0] if top_retweets else 0,
            "cpc": fetch_cpc_dummy(keyword)
        }
        logging.info(f"Twitter 수집 완료: {keyword} mentions={mentions} top_retweet={result['top_retweet']} cpc={result['cpc']}")
        return result
    except Exception as e:
        logging.error(f"Twitter 에러 '{keyword}': {e}")
        return None

def fetch_youtube_trends(keyword, max_results=20):
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        logging.warning("YouTube API 키가 설정되지 않았습니다.")
        return None
    try:
        search_url = "https://www.googleapis.com/youtube/v3/search"
        search_params = {
            "part": "snippet",
            "q": keyword,
            "type": "video",
            "order": "viewCount",
            "maxResults": max_results,
            "key": api_key
        }
        resp = requests.get(search_url, params=search_params, timeout=10)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        if not items:
            logging.warning(f"YouTube: '{keyword}' 검색 결과 없음")
            return None
        video_ids = ",".join([
            item.get("id", {}).get("videoId")
            for item in items
            if item.get("id", {}).get("videoId")
        ])
        if not video_ids:
            return None
        stats_url = "https://www.googleapis.com/youtube/v3/videos"
        stats_params = {
            "part": "statistics",
            "id": video_ids,
            "key": api_key
        }
        stats_resp = requests.get(stats_url, params=stats_params, timeout=10)
        stats_resp.raise_for_status()
        views = [
            int(v.get("statistics", {}).get("viewCount", 0))
            for v in stats_resp.json().get("items", [])
        ]
        avg_views = sum(views) / len(views) if views else 0
        result = {
            "keyword": keyword,
            "source": "YouTube",
            "avg_views": int(avg_views),
            "cpc": fetch_cpc_dummy(keyword)
        }
        logging.info(
            f"YouTube 수집 완료: {keyword} avg_views={result['avg_views']} cpc={result['cpc']}"
        )
        return result
    except Exception as e:
        logging.error(f"YouTube 에러 '{keyword}': {e}")
        return None


def fetch_instagram_metrics(keyword):
    access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    user_id = os.getenv("INSTAGRAM_USER_ID")
    if not access_token or not user_id:
        logging.warning("Instagram API 자격 증명이 설정되지 않았습니다.")
        return None
    try:
        search_url = "https://graph.facebook.com/v17.0/ig_hashtag_search"
        params = {"user_id": user_id, "q": keyword, "access_token": access_token}
        resp = requests.get(search_url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json().get("data")
        if not data:
            logging.warning(f"Instagram: '{keyword}' 해시태그 없음")
            return None
        tag_id = data[0]["id"]
        top_url = f"https://graph.facebook.com/v17.0/{tag_id}/top_media"
        top_params = {
            "user_id": user_id,
            "fields": "like_count,comments_count",
            "access_token": access_token,
        }
        top_resp = requests.get(top_url, params=top_params, timeout=10)
        top_resp.raise_for_status()
        posts = top_resp.json().get("data", [])
        likes = [p.get("like_count", 0) for p in posts]
        avg_likes = sum(likes) / len(likes) if likes else 0
        result = {
            "keyword": keyword,
            "source": "Instagram",
            "avg_likes": int(avg_likes),
            "cpc": fetch_cpc_dummy(keyword),
        }
        logging.info(
            f"Instagram 수집 완료: {keyword} avg_likes={result['avg_likes']} cpc={result['cpc']}"
        )
        return result
    except Exception as e:
        logging.error(f"Instagram 에러 '{keyword}': {e}")
        return None


def fetch_tiktok_metrics(keyword):
    token = os.getenv("TIKTOK_API_TOKEN")
    if not token:
        logging.warning("TikTok API 토큰이 설정되지 않았습니다.")
        return None
    try:
        # 예시용 엔드포인트. 실제 API 스펙에 맞게 수정 필요
        url = "https://open.tiktokapis.com/v2/post/published-list/"
        params = {"keyword": keyword, "access_token": token}
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        views = [int(v.get("play_count", 0)) for v in data]
        avg_views = sum(views) / len(views) if views else 0
        result = {
            "keyword": keyword,
            "source": "TikTok",
            "avg_views": int(avg_views),
            "cpc": fetch_cpc_dummy(keyword),
        }
        logging.info(
            f"TikTok 수집 완료: {keyword} avg_views={result['avg_views']} cpc={result['cpc']}"
        )
        return result
    except Exception as e:
        logging.error(f"TikTok 에러 '{keyword}': {e}")
        return None

# ---------------------- 필터링 함수 ----------------------
def filter_keywords(entries):
    filtered = []
    for item in entries:
        source = item.get("source", "")
        cpc = item.get("cpc", 0)

        if source == "GoogleTrends":
            if (item.get("score", 0) >= GOOGLE_TRENDS_MIN_SCORE and
                item.get("growth", 0) >= GOOGLE_TRENDS_MIN_GROWTH and
                cpc >= MIN_CPC):
                filtered.append(item)

        elif source == "Twitter":
            if (item.get("mentions", 0) >= TWITTER_MIN_MENTIONS and
                item.get("top_retweet", 0) >= TWITTER_MIN_TOP_RETWEET and
                cpc >= MIN_CPC):
                filtered.append(item)

        elif source == "YouTube":
            if item.get("avg_views", 0) >= YOUTUBE_MIN_AVG_VIEWS and cpc >= MIN_CPC:
                filtered.append(item)

        elif source == "Instagram":
            if item.get("avg_likes", 0) >= INSTAGRAM_MIN_AVG_LIKES and cpc >= MIN_CPC:
                filtered.append(item)

        elif source == "TikTok":
            if item.get("avg_views", 0) >= TIKTOK_MIN_AVG_VIEWS and cpc >= MIN_CPC:
                filtered.append(item)

    logging.info(f"필터링된 키워드 개수: {len(filtered)}")
    return filtered

# ---------------------- 키워드별 수집 작업 ----------------------
def collect_data_for_keyword(keyword, pytrends):
    results = []
    try:
        gtrend = fetch_google_trends(keyword, pytrends)
        if gtrend:
            results.append(gtrend)
    except Exception as e:
        logging.error(f"Google Trends 처리 실패: {keyword} - {e}")

    try:
        twitter = fetch_twitter_metrics(keyword)
        if twitter:
            results.append(twitter)
    except Exception as e:
        logging.error(f"Twitter 처리 실패: {keyword} - {e}")

    try:
        youtube = fetch_youtube_trends(keyword)
        if youtube:
            results.append(youtube)
    except Exception as e:
        logging.error(f"YouTube 처리 실패: {keyword} - {e}")

    try:
        insta = fetch_instagram_metrics(keyword)
        if insta:
            results.append(insta)
    except Exception as e:
        logging.error(f"Instagram 처리 실패: {keyword} - {e}")

    try:
        tiktok = fetch_tiktok_metrics(keyword)
        if tiktok:
            results.append(tiktok)
    except Exception as e:
        logging.error(f"TikTok 처리 실패: {keyword} - {e}")

    return results

# ---------------------- 메인 파이프라인 ----------------------
def run_pipeline():
    keywords = generate_keyword_pairs(TOPIC_DETAILS)
    pytrends = TrendReq(hl='ko', tz=540)
    all_results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(collect_data_for_keyword, kw, pytrends): kw for kw in keywords}

        for future in as_completed(futures):
            kw = futures[future]
            try:
                data = future.result()
                all_results.extend(data)
            except Exception as e:
                logging.error(f"{kw} 처리 중 에러: {e}")

    filtered = filter_keywords(all_results)
    result = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "filtered_keywords": filtered
    }

    try:
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        logging.info(f"✅ 결과 저장 완료: {OUTPUT_PATH}")
    except Exception as e:
        logging.error(f"결과 저장 실패: {e}")

if __name__ == "__main__":
    run_pipeline()
