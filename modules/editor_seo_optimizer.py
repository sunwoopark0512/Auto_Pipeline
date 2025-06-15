"""Optimize generated text for SEO using OpenAI."""

from openai import OpenAI


def optimize_text(text: str, target_tone: str = "friendly") -> str:
    """Improve grammar, style and SEO of ``text`` using OpenAI."""

    client = OpenAI()
    prompt = (
        "Revise the following text to improve grammar, style, and SEO. "
        f"Use a {target_tone} tone:\n\n{text}"
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content or ""
    return content.strip()
