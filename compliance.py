"""Utility to check text against banned or restricted terms for each platform."""

from typing import List, Tuple

# Terms can be customised per platform.
PLATFORM_TERMS = {
    "notion": {
        "banned": ["spam", "scam"],
        "restricted": ["clickbait"]
    },
    "generation": {
        "banned": [],
        "restricted": []
    }
}


def scan_text(text: str, platform: str = "notion") -> List[str]:
    """Return list of banned or restricted terms found in the text."""
    terms = PLATFORM_TERMS.get(platform, {})
    banned_terms = terms.get("banned", []) + terms.get("restricted", [])
    found = [term for term in banned_terms if term.lower() in text.lower()]
    return found


def is_compliant(text: str, platform: str = "notion") -> Tuple[bool, List[str]]:
    """Check whether text is compliant for the given platform."""
    found = scan_text(text, platform)
    return len(found) == 0, found
