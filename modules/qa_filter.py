"""Content QA utilities using OpenAI."""

from openai import OpenAI


def content_safety_check(text: str) -> bool:
    """Check generated text for policy violations."""

    client = OpenAI()
    prompt = (
        "Does this content violate any community guidelines or contain "
        f"offensive terms?\n\n{text}\n\nReply YES or NO."
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content or ""
    return "YES" not in content.upper()
