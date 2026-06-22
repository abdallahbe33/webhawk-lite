import html
import re
from urllib.parse import unquote


XSS_PATTERNS = [
    re.compile(
        r"<\s*script\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"<\s*/\s*script\s*>",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bon\w+\s*=",
        re.IGNORECASE,
    ),
    re.compile(
        r"javascript\s*:",
        re.IGNORECASE,
    ),
    re.compile(
        r"<\s*(?:iframe|object|embed|svg|img)\b",
        re.IGNORECASE,
    ),
]


def detect_xss(value):
    text = str(value or "")

    decoded_text = html.unescape(
        unquote(text)
    )

    for pattern in XSS_PATTERNS:
        if pattern.search(decoded_text):
            return True

    return False