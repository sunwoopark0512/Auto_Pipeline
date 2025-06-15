import openai
from typing import List

openai.api_key = "YOUR_API_KEY"  # Replace with actual key or environment variable


def generate_blog_post(topic: str, outline: List[str]) -> str:
    """Generate a blog post draft using an LLM.

    Args:
        topic: Main topic of the post.
        outline: List of bullet points for the post.
    Returns:
        Generated blog post text.
    """
    prompt = f"Topic: {topic}\nOutline: {'; '.join(outline)}\nWrite a blog post about this topic."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message["content"]
