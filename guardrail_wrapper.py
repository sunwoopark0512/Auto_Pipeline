from guardrails import Guard
from openai import OpenAI
import os

client = OpenAI()
guard = Guard.from_yaml("llm_monitor/guardrail_schema.yml")

def safe_completion(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    validated = guard(
        response=response.choices[0].message.content,
        prompt_params={"prompt": prompt}
    )
    return validated["safe_response"]
