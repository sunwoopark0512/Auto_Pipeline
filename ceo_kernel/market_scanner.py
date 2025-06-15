"""Market scanning utilities using the OpenAI API."""

import os
import openai


def _build_client() -> openai.OpenAI:
    """Create an OpenAI client using an environment key or dummy value."""
    return openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY", "sk-dummy"))


client = _build_client()

def scan_market(niche: str) -> str:
    """Scan SaaS opportunities in a given niche."""
    query = f"List SaaS opportunities in {niche} with gaps."
    completion = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": query}]
    )
    content = completion.choices[0].message.content or ""
    return str(content)

if __name__ == "__main__":
    print(scan_market("AI writing tools"))
