import os
import sys
import pytest
from jsonschema import ValidationError, validate

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from schemas import KEYWORD_OUTPUT_SCHEMA, HOOK_OUTPUT_SCHEMA


def test_keyword_schema_valid():
    data = {
        "timestamp": "2024-01-01T00:00:00Z",
        "filtered_keywords": [
            {
                "keyword": "여행 국내여행",
                "source": "GoogleTrends",
                "score": 70,
                "growth": 1.5,
                "cpc": 1200,
            },
            {
                "keyword": "다이어트 홈트",
                "source": "Twitter",
                "mentions": 40,
                "top_retweet": 60,
                "cpc": 1500,
            },
        ],
    }
    validate(data, KEYWORD_OUTPUT_SCHEMA)


def test_keyword_schema_invalid():
    invalid = {"timestamp": "2024-01-01"}
    with pytest.raises(ValidationError):
        validate(invalid, KEYWORD_OUTPUT_SCHEMA)


def test_hook_schema_valid():
    hooks = [
        {
            "keyword": "여행 국내여행",
            "hook_prompt": "prompt",
            "timestamp": "2024-01-01T00:00:00Z",
            "hook_lines": ["a", "b"],
            "blog_paragraphs": ["p1", "p2", "p3"],
            "video_titles": ["t1", "t2"],
            "generated_text": "all\ntext",
        }
    ]
    validate(hooks, HOOK_OUTPUT_SCHEMA)


def test_hook_schema_invalid():
    hooks = [{"keyword": "test"}]
    with pytest.raises(ValidationError):
        validate(hooks, HOOK_OUTPUT_SCHEMA)
