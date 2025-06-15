"""Data models used within the pipeline."""

from typing import List

from pydantic import BaseModel, Field


class HookItem(BaseModel):
    """Structured representation of a generated marketing hook."""

    keyword: str
    hook_lines: List[str] = Field(min_items=2, max_items=2)
    blog_paragraphs: List[str]
    video_titles: List[str]
    source: str
    score: int
