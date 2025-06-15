from openai import OpenAI

client = OpenAI()

_PLAT_PROMPT = {
    "instagram":  "Create an engaging Instagram caption with 3 relevant hashtags.",
    "twitter":    "Write a concise tweet (max 280 chars) with 2 trending hashtags.",
    "linkedin":   "Draft a professional LinkedIn post teaser (max 600 chars).",
    "youtube":    "Generate a compelling YouTube video description (max 1000 chars).",
}

def generate_caption(platform: str, summary: str) -> str:
    prompt = f"{_PLAT_PROMPT[platform]}\n\nContent:\n{summary}"
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content.strip()
