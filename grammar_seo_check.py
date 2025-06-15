#!/usr/bin/env python3
"""Utilities for grammar checking, SEO keyword counting and readability scoring.

This module provides a simple wrapper around the LanguageTool API for grammar
checking, counts occurrences of given SEO keywords, and computes several
readability metrics using ``textstat``.

It exposes a :func:`run_check` helper that prints a summary for a given file.
"""
# pylint: disable=no-member

from __future__ import annotations

import json
import os
from typing import Dict, List

import requests
import textstat  # type: ignore


def grammar_check_languagetool(text: str, lang: str = "en-US") -> List[dict]:
    """Return grammar/style issues from the LanguageTool API."""
    url = "https://api.languagetoolplus.com/v2/check"
    payload = {"text": text, "language": lang, "enabledOnly": False}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers, timeout=15)
    response.raise_for_status()
    return response.json().get("matches", [])


def readability_score(text: str) -> Dict[str, float]:
    """Compute common readability metrics for ``text``."""
    return {
        "Flesch Reading Ease": textstat.flesch_reading_ease(text),
        "Flesch-Kincaid Grade": textstat.flesch_kincaid_grade(text),
        "Gunning Fog": textstat.gunning_fog(text),
        "SMOG Index": textstat.smog_index(text),
        "Dale-Chall Score": textstat.dale_chall_readability_score(text),
    }


def seo_keyword_check(text: str, keyword_list: List[str]) -> Dict[str, int]:
    """Count how often each keyword from ``keyword_list`` appears in ``text``."""
    lowered = text.lower()
    return {kw: lowered.count(kw.lower()) for kw in keyword_list}


def run_check(
    filepath: str = "generated_articles/sample.md",
    keyword_file: str = "config/seo_keywords.json",
) -> None:
    """Run grammar, SEO, and readability checks for ``filepath``."""
    if not os.path.exists(filepath):
        print("❌ 파일이 존재하지 않습니다:", filepath)
        return

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    grammar_results = grammar_check_languagetool(text)
    print(f"✍ 문법 이슈 {len(grammar_results)}건 발견")

    if os.path.exists(keyword_file):
        with open(keyword_file, "r", encoding="utf-8") as f:
            keyword_data = json.load(f)
        keywords = keyword_data.get("priority_keywords", [])
    else:
        keywords = []

    seo_result = seo_keyword_check(text, keywords)
    readability = readability_score(text)

    print("\n📈 SEO 키워드 등장 횟수:")
    for kw, cnt in seo_result.items():
        print(f"  - {kw}: {cnt}회")

    print("\n📊 읽기 난이도 점수:")
    for metric, score in readability.items():
        print(f"  - {metric}: {score:.2f}")


if __name__ == "__main__":
    run_check()
