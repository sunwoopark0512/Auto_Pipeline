#!/usr/bin/env python3
"""
idea_scraper.py
트렌드 기반 키워드 및 후킹 문구를 자동 수집하는 모듈
- Google Trends + YouTube 자동 연동
- TikTok, X 등의 API는 커스텀 함수로 확장 가능
"""

import requests
import datetime
from bs4 import BeautifulSoup
from typing import List, Dict


def fetch_google_trends(keyword: str, geo: str = 'KR', timeframe: str = 'now 7-d') -> List[str]:
    """Google Trends에서 관련 트렌드 키워드를 가져옵니다."""
    from pytrends.request import TrendReq

    pytrends = TrendReq(hl='ko', tz=540)
    pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo, gprop='')
    suggestions = pytrends.related_queries()[keyword]['top']
    if suggestions is not None:
        return suggestions['query'].tolist()
    return []


def fetch_youtube_autocomplete(keyword: str) -> List[str]:
    """YouTube 검색 자동완성 결과 수집 (비공식 API 기반)"""
    url = f"https://suggestqueries.google.com/complete/search?client=youtube&ds=yt&q={keyword}&hl=ko"
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()[1]
    return []


def generate_hooks_from_keywords(keywords: List[str]) -> List[str]:
    """키워드 기반 후킹 문구 생성 (단순 템플릿 활용)"""
    hooks = []
    for kw in keywords:
        hooks.append(f"{kw} 때문에 모두가 놀랐다!?")
        hooks.append(f"당신도 {kw} 하고 있나요?")
        hooks.append(f"지금 {kw} 안 하면 손해입니다.")
    return hooks


def save_keywords_to_file(data: Dict[str, List[str]], filename: str = "prompt_library/idea_capture_prompts.json"):
    """결과 저장"""
    import json
    import os

    os.makedirs("prompt_library", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def run_scraper(seed_keyword: str = "여행", geo: str = "KR"):
    """스크래퍼 실행 함수"""
    google_keywords = fetch_google_trends(seed_keyword, geo=geo)
    youtube_suggestions = fetch_youtube_autocomplete(seed_keyword)
    merged = list(set(google_keywords + youtube_suggestions))
    hooks = generate_hooks_from_keywords(merged)
    data = {
        "seed": seed_keyword,
        "timestamp": str(datetime.datetime.now()),
        "trends": merged,
        "hooks": hooks,
    }
    save_keywords_to_file(data)
    print(f"✅ 트렌드 키워드 {len(merged)}개 수집 및 저장 완료.")


if __name__ == "__main__":
    run_scraper("여행")
