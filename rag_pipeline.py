#!/usr/bin/env python3
"""
rag_pipeline.py
RAG 기반 원고 자동 생성기:
1. 키워드 기반 실시간 웹 검색
2. 요약 정리 및 GPT에 전달
3. SEO 친화적 원고 자동 생성
"""

import json
import os
from typing import List

import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # 환경변수에서 불러오기


def search_web(query: str, num_results: int = 3) -> List[str]:
    """Perplexity API 또는 Bing/SerpAPI로 대체 가능"""
    # 여기서는 예시로 Serper.dev API 사용
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": os.getenv("SERPER_API_KEY"),
        "Content-Type": "application/json",
    }
    payload = {"q": query, "num": num_results}
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
    results = response.json()
    return [r["snippet"] for r in results.get("organic", [])]


def summarize_context(snippets: List[str]) -> str:
    """검색 결과 요약"""
    context = "\n".join(snippets)
    return f"다음 정보를 바탕으로 요약해줘:\n{context}"


def generate_article(topic: str, context_summary: str) -> str:
    """GPT를 활용한 SEO 친화적 원고 자동 생성"""
    prompt = f"""당신은 SEO 최적화 콘텐츠 작가입니다.
주제: {topic}
배경 정보: {context_summary}
위 정보를 바탕으로 흥미롭고 구조화된 블로그 원고를 작성하세요.
형식: 제목 + 부제목 + 본문 (3~5 문단)"""

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"},
        json={
            "model": "gpt-4",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        },
        timeout=30,
    )
    return response.json()["choices"][0]["message"]["content"]


def save_article(title: str, content: str, filename: str | None = None) -> None:
    """원고 저장 (Markdown)"""
    os.makedirs("generated_articles", exist_ok=True)
    if not filename:
        filename = title.replace(" ", "_") + ".md"
    with open(f"generated_articles/{filename}", "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n{content}")
    print(f"✅ 원고 저장 완료 → generated_articles/{filename}")


def run_rag_pipeline(topic: str) -> None:
    """전체 실행 파이프라인"""
    print(f"🔍 '{topic}' 주제 검색 중...")
    snippets = search_web(topic)
    context = summarize_context(snippets)
    article = generate_article(topic, context)
    save_article(topic, article)


if __name__ == "__main__":
    run_rag_pipeline("2025년 여행 트렌드")
