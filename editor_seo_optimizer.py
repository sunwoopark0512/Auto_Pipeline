# Style and SEO optimization utility
from openai import OpenAI

def optimize_text(text: str, target_tone: str = "friendly") -> str:
    """Return a revised version of *text* with improved grammar, style, and SEO.

    Parameters
    ----------
    text: str
        The original text to be optimized.
    target_tone: str, optional
        Tone of the output text (default: "friendly").
    """
    prompt = (
        f"Revise the following text to improve grammar, style, and SEO. "
        f"Use a {target_tone} tone:\n\n{text}"
    )
    response = OpenAI().chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
