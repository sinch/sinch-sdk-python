import logging
import re
from typing import Any, Dict, Union, Optional
from sinch.domains.authentication.webhooks.v1.authentication_validation import (
    validate_webhook_signature_with_nonce,
)
from sinch.domains.authentication.webhooks.v1.webhook_utils import (
    parse_json,
    normalize_iso_timestamp,
)
from sinch.domains.conversation.models.v1.webhooks import (
    ConversationWebhookEventBase,
    MessageDeliveryReceiptEvent,
    MessageInboundEvent,
    MessageSubmitEvent,
)


logger = logging.getLogger(__name__)


def _charset_from_content_type(headers: Dict[str, str]) -> str:
    """Extract charset from Content-Type header; default to utf-8."""
    ct = (
        (headers or {}).get("content-type")
        or (headers or {}).get("Content-Type")
        or ""
    )
    match = re.search(r"charset\s*=\s*([^\s;]+)", ct, re.I)
    return match.group(1).strip("'\"").lower() if match else "utf-8"


def _decode_payload(
    payload: Union[str, bytes], headers: Optional[Dict[str, str]] = None
) -> str:
    """Decode payload to str using Content-Type charset when payload is bytes."""
    if isinstance(payload, str):
        return payload
    charset = _charset_from_content_type(headers or {}) if headers else "utf-8"
    try:
        return payload.decode(charset)
    except (LookupError, UnicodeDecodeError):
        return payload.decode("utf-8")


ConversationWebhookCallback = Union[
    MessageDeliveryReceiptEvent,
    MessageInboundEvent,
    MessageSubmitEvent,
    ConversationWebhookEventBase,
]


class ConversationWebhooks:
    """
    Handler for Conversation API webhooks: validate signature and parse events.
    """

    def __init__(self, webhook_secret: Optional[str] = None):
        """
        :param webhook_secret: Secret configured for the webhook (used for HMAC validation).
        """
        self.webhook_secret = webhook_secret

    def _validate_signature(
        self,
        payload: Union[str, bytes],
        headers: Dict[str, str],
        webhook_secret: Optional[str] = None,
    ) -> bool:
        """
        Validate the webhook signature using the request body and headers.

        Uses x-sinch-webhook-signature, x-sinch-webhook-signature-nonce, and
        x-sinch-webhook-signature-timestamp. Returns True only if the signature
        is valid.

        :param payload: Raw request body (string or bytes).
        :param headers: Incoming request headers (key case is normalized to lower).
        :param webhook_secret: Secret for this webhook; defaults to the secret passed to __init__.
        :returns: True if the signature is valid, False otherwise.
        """
        secret = (
            webhook_secret
            if webhook_secret is not None
            else self.webhook_secret
        )
        if not secret:
            return False
        payload_str = _decode_payload(payload, headers)
        return validate_webhook_signature_with_nonce(
            secret, headers, payload_str
        )

    def validate_authentication_header(
        self, headers: Dict[str, str], json_payload: str
    ) -> bool:
        """
        Validate the webhook signature (convenience wrapper around internal validation).

        :param headers: Incoming request's headers.
        :param json_payload: Incoming request's raw body.
        :returns: True if the X-Sinch-Webhook-Signature header is valid.
        """
        return self._validate_signature(json_payload, headers)

    def parse_event(
        self, event_body: Union[str, Dict[str, Any]]
    ) -> ConversationWebhookCallback:
        """
        Parse the webhook payload into a typed event.

        Parses by key: message_delivery_report → MessageDeliveryReceiptEvent,
        message → MessageInboundEvent, message_submit_notification → MessageSubmitEvent.
        Normalizes accepted_time and event_time. Injects trigger on the returned event.

        :param event_body: JSON string or dict of the webhook body.
        :returns: Parsed event model.
        :raises ValueError: If JSON parsing fails or the payload is invalid.
        """
        if isinstance(event_body, str):
            event_body = parse_json(event_body)

        # Normalize timestamp fields
        for key in ("accepted_time", "event_time"):
            if key in event_body and isinstance(event_body[key], str):
                event_body[key] = normalize_iso_timestamp(event_body[key])

        # Type is determined by which key is present (message_delivery_report, message,
        # message_submit_notification).
        if "message_delivery_report" in event_body:
            return MessageDeliveryReceiptEvent(**event_body)
        if "message" in event_body:
            return MessageInboundEvent(**event_body)
        if "message_submit_notification" in event_body:
            return MessageSubmitEvent(**event_body)

        logger.warning(
            "Conversation webhook: unknown event type; returning base event."
        )
        return ConversationWebhookEventBase(**event_body)
