import base64
import hashlib
import hmac
import json
import re
from typing import Any, Dict, Optional, Tuple, Union


def normalize_headers(headers: Dict[str, str]) -> Dict[str, str]:
    """
    Normalize headers by lower-casing their keys and dropping ``None`` values.

    :param headers: Incoming request's headers.
    :type headers: Dict[str, str]
    :returns: Normalized headers.
    :rtype: Dict[str, str]
    """
    return {k.lower(): v for k, v in headers.items() if v is not None}


def get_header(header_value: Optional[Union[str, list]]) -> Optional[str]:
    """
    Extract a single header value, unwrapping a list if the transport provides one.

    :param header_value: Raw header value.
    :type header_value: Optional[Union[str, list]]
    :returns: The header value, or ``None`` if absent.
    :rtype: Optional[str]
    """
    if header_value is None:
        return None
    if isinstance(header_value, list):
        return header_value[0] if header_value else None
    return header_value


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


def check_authorization_header_format(authorization: str) -> Optional[Tuple[str, str]]:
    """
    Split an ``Authorization`` header into its scheme and value.

    :param authorization: Raw ``Authorization`` header value.
    :type authorization: str
    :returns: A ``(scheme, value)`` tuple, or ``None`` if the header has no scheme part.
    :rtype: Optional[Tuple[str, str]]
    """
    parts = authorization.split(" ", 1)
    if len(parts) != 2:
        return None
    return parts[0], parts[1]


def compute_content_md5(body: Union[str, bytes]) -> str:
    """
    Compute the Base64-encoded MD5 digest of a request body.

    :param body: Request body.
    :type body: Union[str, bytes]
    :returns: Base64-encoded MD5 digest.
    :rtype: str
    """
    body_bytes = body.encode("utf-8") if isinstance(body, str) else body
    return base64.b64encode(hashlib.md5(body_bytes).digest()).decode("utf-8")


def build_string_to_sign(
    method: str,
    content_md5: str,
    content_type: str,
    timestamp: str,
    path: str,
) -> str:
    """
    Build the canonical string signed by the service/application signature scheme.

    :param method: HTTP method of the incoming request.
    :type method: str
    :param content_md5: Base64-encoded MD5 digest of the request body.
    :type content_md5: str
    :param content_type: Value of the ``Content-Type`` header.
    :type content_type: str
    :param timestamp: Value of the ``X-Timestamp`` header.
    :type timestamp: str
    :param path: Canonicalized resource path of the incoming request.
    :type path: str
    :returns: The string to sign.
    :rtype: str
    """
    return "\n".join([method, content_md5, content_type, f"x-timestamp:{timestamp}", path])


def compute_signature(string_to_sign: str, secret: str) -> str:
    """
    Compute the Base64-encoded HMAC-SHA256 signature for the service/application scheme.

    :param string_to_sign: The canonical string to sign.
    :type string_to_sign: str
    :param secret: Base64-encoded secret.
    :type secret: str
    :returns: Base64-encoded signature.
    :rtype: str
    """
    key = base64.b64decode(secret)
    digest = hmac.new(key, string_to_sign.encode("utf-8"), hashlib.sha256).digest()
    return base64.b64encode(digest).decode("utf-8")
