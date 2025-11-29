import json
import re
from datetime import datetime
from typing import Any, Dict


def parse_json(payload: str) -> Dict[str, Any]:
    """
    Parse JSON string into a dictionary.

    :param payload: JSON string to parse.
    :type payload: str
    :returns: Parsed dictionary.
    :rtype: Dict[str, Any]
    :raises ValueError: If JSON parsing fails.
    """
    try:
        return json.loads(payload)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode JSON: {e}")


def normalize_iso_timestamp(timestamp: str) -> datetime:
    """
    Normalize a timestamp string to ensure compatibility with Python's `datetime.fromisoformat()`.

    - Ensures that the timestamp includes a UTC offset (e.g., "+00:00") if missing.
    - Replaces trailing "Z" with "+00:00" to indicate UTC.
    - Trims microseconds to 6 digits.

    :param timestamp: Timestamp string to normalize.
    :type timestamp: str
    :returns: Timezone-aware datetime object.
    :rtype: datetime
    :raises ValueError: If timestamp format is invalid.
    """
    if timestamp.endswith("Z"):
        timestamp = timestamp.replace("Z", "+00:00")
    elif not re.search(r"(Z|[+-]\d{2}:?\d{2})$", timestamp):
        timestamp += "+00:00"
    match_ms = re.search(r"\.(\d{7,})(?=[+-])", timestamp)
    if match_ms:
        micro_trimmed = match_ms.group(1)[:6]
        timestamp = re.sub(
            r"\.\d{7,}(?=[+-])", f".{micro_trimmed}", timestamp
        )
    try:
        return datetime.fromisoformat(timestamp)
    except ValueError as e:
        raise ValueError(f"Invalid timestamp format: {e}")
