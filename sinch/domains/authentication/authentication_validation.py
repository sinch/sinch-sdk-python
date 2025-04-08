import hashlib
import hmac
from typing import Dict, Union, Optional, List
from pydantic import StrictStr, StrictBool


def validate_signature_header(
    callback_secret: StrictStr,
    headers: Dict[StrictStr, StrictStr],
    body: StrictStr
) -> StrictBool:
    """
    Validate signature headers for Numbers callback.

    Note: A ``callback_url`` must be associated with the number.

    :param callback_secret: Secret associated with the rented number.
    :type callback_secret: StrictStr
    :param headers: Incoming request's headers.
    :type headers: Dict[StrictStr, StrictStr]
    :param body: Incoming request's body.
    :type body: StrictStr
    :returns: True if the signature header is valid.
    :rtype: StrictBool
    """

    normalized_headers = normalize_headers(headers)
    signature = get_header(normalized_headers.get('x-sinch-signature'))
    if signature is None:
        return False

    expected_signature = compute_hmac_signature(body, callback_secret)
    return signature == expected_signature


def normalize_headers(headers: Dict[StrictStr, StrictStr]) -> Dict[StrictStr, StrictStr]:
    """
    Normalize headers by converting keys to lowercase and filtering out None values
    """
    return {k.lower(): v for k, v in headers.items() if v is not None}


def compute_hmac_signature(body: StrictStr, secret: StrictStr) -> StrictStr:
    """
    Compute HMAC-SHA1 signature
    """
    return hmac.new(
        key=secret.encode('utf-8'),
        msg=body.encode('utf-8') if isinstance(body, str) else body,
        digestmod=hashlib.sha1
    ).hexdigest()


def get_header(header_value: Optional[Union[StrictStr, List[StrictStr]]]) -> Optional[StrictStr]:
    """
    Extract header value, handling both string and list cases
    """
    if header_value is None:
        return None
    if isinstance(header_value, list):
        return header_value[0] if header_value else None
    return header_value
