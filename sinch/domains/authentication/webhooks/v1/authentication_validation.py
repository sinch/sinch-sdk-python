import hashlib
import hmac
from typing import Dict, Union, Optional, List


def validate_signature_header(
    callback_secret: str,
    headers: Dict[str, str],
    body: str
) -> bool:
    """
    Validate signature headers for Numbers callback.

    Note: A ``callback_url`` must be associated with the number.

    :param callback_secret: Secret associated with the rented number.
    :type callback_secret: str
    :param headers: Incoming request's headers.
    :type headers: Dict[str, str]
    :param body: Incoming request's body.
    :type body: str
    :returns: True if the signature header is valid.
    :rtype: bool
    """

    normalized_headers = normalize_headers(headers)
    signature = get_header(normalized_headers.get('x-sinch-signature'))
    if signature is None:
        return False

    expected_signature = compute_hmac_signature(body, callback_secret)
    return signature == expected_signature


def normalize_headers(headers: Dict[str, str]) -> Dict[str, str]:
    """
    Normalize headers by converting keys to lowercase and filtering out None values
    """
    return {k.lower(): v for k, v in headers.items() if v is not None}


def compute_hmac_signature(body: str, secret: str) -> str:
    """
    Compute HMAC-SHA1 signature
    """
    return hmac.new(
        key=secret.encode('utf-8'),
        msg=body.encode('utf-8') if isinstance(body, str) else body,
        digestmod=hashlib.sha1
    ).hexdigest()


def get_header(header_value: Optional[Union[str, List[str]]]) -> Optional[str]:
    """
    Extract header value, handling both string and list cases
    """
    if header_value is None:
        return None
    if isinstance(header_value, list):
        return header_value[0] if header_value else None
    return header_value
