"""Simple competitor analysis using OpenAI."""

import os
import openai


def _build_client() -> openai.OpenAI:
    return openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY", "sk-dummy"))


client = _build_client()

def analyze_competitor(name: str) -> str:
    """Summarize competitor SaaS information."""
    prompt = f"Summarize {name} SaaS business model, pricing, weak points."
    completion = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}]
    )
    content = completion.choices[0].message.content or ""
    return str(content)

if __name__ == "__main__":
    print(analyze_competitor("Example SaaS"))
