"""Rewrite underperforming titles or text to improve CTR."""
from openai import OpenAI

client = OpenAI()


def rewrite_for_performance(title: str, fail_reason: str) -> str:
    """Return a rewritten title addressing the given failure reason."""
    prompt = (
        f"The following title under-performed ({fail_reason}). "
        "Rewrite it to be more eye-catching, max 60 chars:\n\n"
        f"Original: {title}"
    )
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content.strip()
