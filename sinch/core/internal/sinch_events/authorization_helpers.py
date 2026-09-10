import hmac
from typing import Dict, Optional, Union

from sinch.core.internal.sinch_events.utils import (
    build_string_to_sign,
    check_authorization_header_format,
    compute_content_md5,
    compute_signature,
    get_header,
    normalize_headers,
)


def validate_authentication_header(
    key: str,
    secret: str,
    headers: Dict[str, str],
    body: Union[str, bytes],
    path: str,
    method: str,
) -> bool:
    """
    Validate the ``Authorization`` header of an application/service-signed sinch event request.

    :param key: Expected service/application key; when given, it must match the header.
    :type key: str
    :param secret: Base64-encoded secret used to sign the request.
    :type secret: str
    :param headers: Incoming request's headers.
    :type headers: Dict[str, str]
    :param body: Incoming request's raw body.
    :type body: Union[str, bytes]
    :param path: Canonicalized resource path of the incoming request.
    :type path: str
    :param method: HTTP method of the incoming request.
    :type method: str
    :returns: True if the Authorization header is present, well-formed, and valid.
    :rtype: bool
    """
    normalized_headers = normalize_headers(headers)
    authorization = get_header(normalized_headers.get("authorization"))
    if authorization is None:
        return False

    auth_parts = check_authorization_header_format(authorization)
    if auth_parts is None:
        return False

    scheme, credentials = auth_parts
    if scheme.lower() == "service":
        return _validate_service_scheme(
            credentials, normalized_headers, key, secret, path, body, method
        )
    return False


def _validate_service_scheme(
    credentials: str,
    normalized_headers: Dict[str, str],
    service_id: str,
    service_secret: str,
    path: str,
    body: Union[str, bytes],
    method: str,
) -> bool:
    """Validate the ``{serviceKey}:{Signature}`` Authorization scheme."""
    key_and_signature = credentials.split(":", 1)
    if len(key_and_signature) != 2:
        return False
    received_key, received_signature = key_and_signature

    if not hmac.compare_digest(received_key, service_id):
        return False

    content_type = get_header(normalized_headers.get("content-type"))
    timestamp = get_header(normalized_headers.get("x-timestamp"))
    if content_type is None or timestamp is None:
        return False

    content_md5 = compute_content_md5(body)
    string_to_sign = build_string_to_sign(
        method.upper(), content_md5, content_type, timestamp, path
    )
    expected_signature = compute_signature(string_to_sign, service_secret)
    return hmac.compare_digest(received_signature, expected_signature)
