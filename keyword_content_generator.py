"""Utility to generate SEO-friendly keywords using OpenAI."""

from openai import OpenAI  # pylint: disable=import-error


def generate_keywords(topic: str, tone: str = "trendy") -> list[str]:
    """Generate SEO-friendly keywords using OpenAI."""
    prompt = f"Generate 10 {tone} SEO-optimized keywords for the topic: '{topic}'"
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    # Split lines and filter out any empty strings
    return [kw.strip() for kw in response.choices[0].message.content.split("\n") if kw.strip()]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate keyword ideas via OpenAI")
    parser.add_argument("topic", help="Topic to generate keywords for")
    parser.add_argument("--tone", default="trendy", help="Tone for the keywords")
    args = parser.parse_args()
    for kw in generate_keywords(args.topic, args.tone):
        print(kw)
