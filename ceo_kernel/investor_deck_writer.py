"""Automatically draft investor pitch decks using OpenAI."""

import os
import openai


def _build_client() -> openai.OpenAI:
    return openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY", "sk-dummy"))


client = _build_client()

def draft_pitch(saas_name: str, metrics: str) -> str:
    """Generate an investor pitch deck outline."""
    prompt = f"Write investor pitch deck for {saas_name} with metrics: {metrics}"
    completion = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}]
    )
    content = completion.choices[0].message.content or ""
    return str(content)

if __name__ == "__main__":
    print(draft_pitch("My SaaS", "users:1000, MRR:$10k"))
