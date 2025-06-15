"""JSON schema definitions for pipeline outputs."""

from typing import Any, Dict

KEYWORD_OUTPUT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "timestamp": {"type": "string"},
        "filtered_keywords": {
            "type": "array",
            "items": {
                "oneOf": [
                    {"$ref": "#/definitions/google_trend"},
                    {"$ref": "#/definitions/twitter"}
                ]
            }
        },
    },
    "required": ["timestamp", "filtered_keywords"],
    "definitions": {
        "base": {
            "type": "object",
            "properties": {
                "keyword": {"type": "string"},
                "source": {"type": "string"},
                "cpc": {"type": "number"},
            },
            "required": ["keyword", "source", "cpc"],
        },
        "google_trend": {
            "allOf": [
                {"$ref": "#/definitions/base"},
                {
                    "properties": {
                        "source": {"const": "GoogleTrends"},
                        "score": {"type": "number"},
                        "growth": {"type": "number"},
                    },
                    "required": ["score", "growth"],
                },
            ]
        },
        "twitter": {
            "allOf": [
                {"$ref": "#/definitions/base"},
                {
                    "properties": {
                        "source": {"const": "Twitter"},
                        "mentions": {"type": "number"},
                        "top_retweet": {"type": "number"},
                    },
                    "required": ["mentions", "top_retweet"],
                },
            ]
        },
    },
}

HOOK_OUTPUT_SCHEMA: Dict[str, Any] = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "keyword": {"type": "string"},
            "hook_prompt": {"type": "string"},
            "timestamp": {"type": "string"},
            "hook_lines": {
                "type": "array",
                "items": {"type": "string"},
            },
            "blog_paragraphs": {
                "type": "array",
                "items": {"type": "string"},
            },
            "video_titles": {
                "type": "array",
                "items": {"type": "string"},
            },
            "generated_text": {"type": "string"},
        },
        "required": [
            "keyword",
            "hook_prompt",
            "timestamp",
            "hook_lines",
            "blog_paragraphs",
            "video_titles",
            "generated_text",
        ],
    },
}
