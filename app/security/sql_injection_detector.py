import re


SQL_INJECTION_PATTERNS = [
    re.compile(
        r"(?:'|\")\s*(?:or|and)\s+"
        r"['\"\w]*\s*=\s*['\"\w]*",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bunion\s+(?:all\s+)?select\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:drop|alter|truncate)\s+table\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\binsert\s+into\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bdelete\s+from\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bupdate\s+\w+\s+set\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:sleep|benchmark|pg_sleep)\s*\(",
        re.IGNORECASE,
    ),
]


def detect_sql_injection(value):
    text = str(value or "")

    for pattern in SQL_INJECTION_PATTERNS:
        if pattern.search(text):
            return True

    return False