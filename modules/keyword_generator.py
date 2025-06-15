"""Utilities for generating keywords using OpenAI."""

from openai import OpenAI


def generate_keywords(topic: str, tone: str = "trendy") -> list[str]:
    """Generate a list of keywords related to ``topic``."""

    client = OpenAI()
    prompt = f"Generate 10 {tone} SEO-optimized keywords for the topic: '{topic}'"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content or ""
    return content.strip().split("\n")
