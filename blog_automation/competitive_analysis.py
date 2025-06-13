"""Competitive Analysis Module
Monitors competitor content to discover content gaps and strategy insights.
"""

from typing import List, Dict, Any
import logging

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    requests = None  # type: ignore
    BeautifulSoup = None  # type: ignore


def fetch_competitor_content(url: str) -> str:
    """Download HTML content from a competitor page."""
    if requests is None:
        raise RuntimeError("requests package is required for web scraping")
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.text
    except Exception as exc:
        logging.warning("Failed to fetch %s: %s", url, exc)
        return ""


def extract_keywords(html: str) -> List[str]:
    """Simple keyword extraction from HTML title and headings."""
    if BeautifulSoup is None:
        raise RuntimeError("bs4 package is required for HTML parsing")
    soup = BeautifulSoup(html, "html.parser")
    texts = [soup.title.string if soup.title else ""]
    texts += [h.get_text() for h in soup.find_all(["h1", "h2", "h3"])]
    keywords = []
    for text in texts:
        if not text:
            continue
        words = [w.strip() for w in text.split() if len(w) > 2]
        keywords.extend(words)
    return keywords


def find_content_gaps(our_keywords: List[str], competitor_keywords: List[str]) -> List[str]:
    """Identify keywords competitors use that we do not."""
    comp_set = set(k.lower() for k in competitor_keywords)
    our_set = set(k.lower() for k in our_keywords)
    gaps = list(comp_set - our_set)
    return gaps
