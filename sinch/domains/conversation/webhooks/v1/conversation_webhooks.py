from typing import Any, Dict, Union, Optional
from sinch.domains.authentication.webhooks.v1.authentication_validation import (
    validate_webhook_signature_with_nonce,
)
from sinch.domains.authentication.webhooks.v1.webhook_utils import (
    parse_json,
    normalize_iso_timestamp,
)
from sinch.domains.conversation.webhooks.v1.events import (
    ConversationWebhookEventBase,
    MessageDeliveryReceiptEvent,
    MessageInboundEvent,
    MessageSubmitEvent,
)


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

    def validate_signature(
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
        if isinstance(payload, bytes):
            payload = payload.decode("utf-8")
        return validate_webhook_signature_with_nonce(secret, headers, payload)

    def validate_authentication_header(
        self, headers: Dict[str, str], json_payload: str
    ) -> bool:
        """
        Validate the webhook signature (convenience alias for validate_signature).

        :param headers: Incoming request's headers.
        :param json_payload: Incoming request's raw body.
        :returns: True if the X-Sinch-Webhook-Signature header is valid.
        """
        return self.validate_signature(json_payload, headers)

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
        # message_submit_notification). Inject trigger so callers can use event.trigger.
        trigger = event_body.get("trigger")
        if not trigger and "message_delivery_report" in event_body:
            trigger = "MESSAGE_DELIVERY"
        if not trigger and "message" in event_body:
            trigger = "MESSAGE_INBOUND"
        if not trigger and "message_submit_notification" in event_body:
            trigger = "MESSAGE_SUBMIT"

        if trigger == "MESSAGE_DELIVERY":
            event_body = {**event_body, "trigger": "MESSAGE_DELIVERY"}
            return MessageDeliveryReceiptEvent(**event_body)
        if trigger == "MESSAGE_INBOUND":
            event_body = {**event_body, "trigger": "MESSAGE_INBOUND"}
            return MessageInboundEvent(**event_body)
        if trigger == "MESSAGE_SUBMIT":
            event_body = {**event_body, "trigger": "MESSAGE_SUBMIT"}
            return MessageSubmitEvent(**event_body)

        return ConversationWebhookEventBase(**event_body)
