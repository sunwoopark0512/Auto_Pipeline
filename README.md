# Auto_Pipeline

This project provides tools for converting content for different platforms and generates marketing hooks that are uploaded to Notion.

## Environment Setup

1. Copy `.env.example` to `.env` in the project root.
2. Edit `.env` and provide the required credentials such as API keys and database IDs.

The `.env.example` file lists all environment variables used by the scripts.

## Usage

### Content Conversion
You can convert content for different platforms using the `convert_content` function from the `content_converter.py` module.

Supported platforms:
- YouTube
- Instagram
- TikTok
- Facebook
- LinkedIn

Example usage:
```python
from content_converter import convert_content

text = "원소스 멀티유스 전략으로 수익을 극대화하는 방법\n..."
yt_script = convert_content(text, "youtube")
print(yt_script)