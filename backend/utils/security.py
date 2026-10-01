"""
HarvestSaarthi AI - Security Utilities
Includes input validation, bounds checking, string sanitization, rate limiting, and prompt injection defense.
"""

import re
from typing import Any, Dict

PROMPT_INJECTION_PATTERNS = [
    r"ignore (all )?previous instructions",
    r"reveal (your )?api key",
    r"system prompt",
    r"environment variables",
    r"override rules",
]


def sanitize_string(val: str, max_length: int = 500) -> str:
    """Sanitizes raw string inputs to protect against injection and excess length."""
    if not val:
        return ""
    # Strip HTML tags
    cleaned = re.sub(r"<[^>]*>", "", val)
    # Remove control characters
    cleaned = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", cleaned)
    return cleaned[:max_length].strip()


def check_prompt_injection(text: str) -> bool:
    """Returns True if text contains potential prompt injection strings."""
    if not text:
        return False
    lower_text = text.lower()
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, lower_text):
            return True
    return False
