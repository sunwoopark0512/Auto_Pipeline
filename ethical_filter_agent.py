import json
import re
from typing import Dict

HATE_WORDS = [
    "hate", "kill", "stupid", "idiot",
]

MISINFO_PHRASES = [
    "flat earth",
    "vaccines cause autism",
    "covid is a hoax",
]

PRIVACY_PATTERNS = [
    r"\b\d{2,3}-\d{3,4}-\d{4}\b",  # phone numbers
]

LEGAL_RISK_WORDS = [
    "copyright", "lawsuit", "illegal", "libel", "sue",
]

def analyze_content(text: str) -> Dict[str, object]:
    """Analyze the input text and return risk flags."""
    lowered = text.lower()
    hate = any(word in lowered for word in HATE_WORDS)
    misinfo = any(phrase in lowered for phrase in MISINFO_PHRASES)
    privacy = any(re.search(pattern, text) for pattern in PRIVACY_PATTERNS)
    legal = any(word in lowered for word in LEGAL_RISK_WORDS)

    reasons = []
    if hate:
        reasons.append("Potential hate speech detected")
    if misinfo:
        reasons.append("Possible misinformation")
    if privacy:
        reasons.append("May contain private information")
    if legal:
        reasons.append("Content might pose legal liability")

    explanation = "; ".join(reasons) if reasons else "No major risks detected"

    return {
        "hate_speech": hate,
        "misinformation_risk": misinfo,
        "privacy_violation_risk": privacy,
        "legal_liability_risk": legal,
        "explanation": explanation,
    }

if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    result = analyze_content(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
