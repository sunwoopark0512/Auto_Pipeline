"""Generate article content using OpenAI."""

from openai import OpenAI


def generate_article(keyword: str, word_count: int = 600, tone: str = "neutral") -> str:
    """Return an SEO blog article for ``keyword``."""

    client = OpenAI()
    prompt = (
        f"Write a {tone} tone SEO blog post about '{keyword}' in approximately "
        f"{word_count} words."
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content or ""
    return content.strip()
