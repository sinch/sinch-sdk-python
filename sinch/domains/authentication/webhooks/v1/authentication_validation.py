import hashlib
import hmac
import base64
import json
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

    if callback_secret is None:
        return False
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


def validate_webhook_signature_with_nonce(
    callback_secret: str,
    headers: Dict[str, str],
    body: str
) -> bool:
    """
    Validate signature headers for webhook callbacks that use nonce and timestamp.

    :param callback_secret: Secret associated with the webhook.
    :type callback_secret: str
    :param headers: Incoming request's headers.
    :type headers: Dict[str, str]
    :param body: Incoming request's body.
    :type body: str
    :returns: True if the X-Sinch-Webhook-Signature header is valid.
    :rtype: bool
    """
    if callback_secret is None:
        return False
    
    normalized_headers = normalize_headers(headers)
    signature = get_header(normalized_headers.get('x-sinch-webhook-signature'))
    if signature is None:
        return False

    nonce = get_header(normalized_headers.get('x-sinch-webhook-signature-nonce'))
    timestamp = get_header(normalized_headers.get('x-sinch-webhook-signature-timestamp'))
    
    if nonce is None or timestamp is None:
        return False

    body_as_string = body
    if isinstance(body, dict):
        body_as_string = json.dumps(body)

    signed_data = compute_signed_data(body_as_string, nonce, timestamp)
    
    expected_signature = calculate_webhook_signature(signed_data, callback_secret)
    return hmac.compare_digest(signature, expected_signature)


def compute_signed_data(body: str, nonce: str, timestamp: str) -> str:
    """
    Compute signed data for webhook signature validation.
    
    Format: body.nonce.timestamp (with dots as separators)
    """
    return f'{body}.{nonce}.{timestamp}'


def calculate_webhook_signature(signed_data: str, secret: str) -> str:
    """
    Calculate webhook signature using HMAC-SHA256 with Base64 encoding.
    
    :param signed_data: The data to sign (body.nonce.timestamp)
    :type signed_data: str
    :param secret: The secret key for HMAC
    :type secret: str
    :returns: Base64-encoded HMAC-SHA256 signature
    :rtype: str
    """
    return base64.b64encode(
        hmac.new(
            key=secret.encode('utf-8'),
            msg=signed_data.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
    ).decode('utf-8')
