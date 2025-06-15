"""Generate alternative text variants for A/B testing."""
from openai import OpenAI

client = OpenAI()


def generate_variants(text: str, k: int = 2) -> list[str]:
    """Return k alternative variants that may improve CTR."""
    prompt = f"Generate {k} alternative variants that may achieve higher CTR:\n\n«{text}»"
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return [v.strip("- ").strip() for v in resp.choices[0].message.content.split("\n") if v]
