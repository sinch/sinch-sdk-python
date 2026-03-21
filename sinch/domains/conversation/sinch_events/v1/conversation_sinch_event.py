import logging
from typing import Any, Dict, Union, Optional
from sinch.domains.authentication.webhooks.v1.authentication_validation import (
    validate_webhook_signature_with_nonce,
)
from sinch.domains.authentication.webhooks.v1.webhook_utils import (
    decode_payload,
    parse_json,
    normalize_iso_timestamp,
)
from sinch.domains.conversation.models.v1.sinch_events import (
    ConversationSinchEventBase,
    ConversationSinchEventPayload,
    MessageDeliveryReceiptEvent,
    MessageInboundEvent,
    MessageSubmitEvent,
)


logger = logging.getLogger(__name__)


class ConversationSinchEvent:
    """
    Handler for Conversation API Sinch Events: validate signature and parse events.
    """

    def __init__(self, callback_secret: Optional[str] = None):
        """
        :param callback_secret: Secret configured for the event destination (used for HMAC validation).
        """
        self.callback_secret = callback_secret

    def _validate_signature(
        self,
        payload: Union[str, bytes],
        headers: Dict[str, str],
        callback_secret: Optional[str] = None,
    ) -> bool:
        """
        Validate the Sinch Event signature using the request body and headers.

        Uses x-sinch-webhook-signature, x-sinch-webhook-signature-nonce, and
        x-sinch-webhook-signature-timestamp. Returns True only if the signature
        is valid.

        :param payload: Raw request body (string or bytes).
        :param headers: Incoming request headers (key case is normalized to lower).
        :param callback_secret: Secret for this request; defaults to the secret passed to __init__.
        :returns: True if the signature is valid, False otherwise.
        """
        secret = (
            callback_secret
            if callback_secret is not None
            else self.callback_secret
        )
        if not secret:
            return False
        payload_str = decode_payload(payload, headers)
        return validate_webhook_signature_with_nonce(
            secret, headers, payload_str
        )

    def validate_authentication_header(
        self,
        headers: Dict[str, str],
        json_payload: Union[str, bytes],
    ) -> bool:
        """
        Validate the Sinch Event signature (convenience wrapper around internal validation).

        :param headers: Incoming request's headers.
        :param json_payload: Incoming request's raw body (str or bytes).
        :returns: True if the X-Sinch-Webhook-Signature header is valid.
        """
        return self._validate_signature(json_payload, headers)

    def parse_event(
        self,
        event_body: Union[str, bytes, Dict[str, Any]],
        headers: Optional[Dict[str, str]] = None,
    ) -> ConversationSinchEventPayload:
        """
        Parse the Sinch Event payload into a typed event.

        Parses by key: message_delivery_report → MessageDeliveryReceiptEvent,
        message → MessageInboundEvent, message_submit_notification → MessageSubmitEvent.
        Normalizes accepted_time and event_time. Injects trigger on the returned event.

        :param event_body: JSON string, raw bytes, or dict of the event body.
        :param headers: Request headers (used to decode charset when event_body is bytes).
        :returns: Parsed event model.
        :raises ValueError: If JSON parsing fails or the payload is invalid.
        """
        if isinstance(event_body, bytes):
            event_body = parse_json(decode_payload(event_body, headers))
        elif isinstance(event_body, str):
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
            "Conversation Sinch Event: unknown event type; returning base event."
        )
        return ConversationSinchEventBase(**event_body)
