"""SEO content generator module."""
from typing import Any
# ✅ SEO 기반 원고 자동 생성기
from openai import OpenAI


def generate_article(keyword: str, word_count: int = 600, tone: str = "neutral") -> str:
    """Generate an SEO-friendly article using OpenAI's chat completion API.

    Args:
        keyword: The topic keyword for the article.
        word_count: Approximate number of words for the post.
        tone: Desired tone of the article.

    Returns:
        Generated article text.
    """
    prompt = (
        f"Write a {tone} tone SEO blog post about '{keyword}' "
        f"in approximately {word_count} words."
    )
    response: Any = OpenAI().chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()
