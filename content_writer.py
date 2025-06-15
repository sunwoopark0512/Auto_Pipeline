from textwrap import fill


def generate_article(keyword: str, word_count: int = 300) -> str:
    """Generate a dummy article containing the keyword."""
    sentence = f"This article discusses {keyword} in depth. "
    content = (sentence * (word_count // len(sentence.split()))).strip()
    return fill(content, 80)
