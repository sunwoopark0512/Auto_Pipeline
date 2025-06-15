import logging
from typing import List

try:
    import language_tool_python
except ImportError:  # Provide a fallback if library is missing
    language_tool_python = None
    logging.warning("language_tool_python not installed; quality checks disabled")


def grammar_check(text: str) -> List[str]:
    """Check grammar of text and return list of issues."""
    if not language_tool_python:
        return []
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text)
    return [m.message for m in matches]
