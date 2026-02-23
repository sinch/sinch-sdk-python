import json
import re
from datetime import datetime
from typing import Any, Dict, Optional, Union


def _content_type_from_headers(headers: Optional[Dict[str, str]]) -> str:
    """Get Content-Type from headers dict (case-insensitive)."""
    if not headers:
        return ""
    return headers.get("content-type") or headers.get("Content-Type") or ""


def _charset_from_content_type(content_type: str) -> str:
    """Extract charset from Content-Type header; default to utf-8 if missing."""
    if not content_type:
        return "utf-8"
    match = re.search(r"charset\s*=\s*([^\s;]+)", content_type, re.I)
    return match.group(1).strip("'\"").lower() if match else "utf-8"


def decode_payload(
    payload: Union[str, bytes], headers: Optional[Dict[str, str]] = None
) -> str:
    """
    Decode request body to str using Content-Type charset when payload is bytes.

    When payload is str, return as-is. When bytes, use charset from headers
    (default utf-8);
    """
    if isinstance(payload, str):
        return payload
    if not payload:
        return ""
    content_type = _content_type_from_headers(headers)
    charset = _charset_from_content_type(content_type)
    try:
        return payload.decode(charset)
    except (LookupError, UnicodeDecodeError):
        raise


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
