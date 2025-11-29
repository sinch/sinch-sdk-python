import json
from typing import Any, Dict, Union, Optional
from pydantic import TypeAdapter
from sinch.domains.authentication.webhooks.v1.authentication_validation import (
    validate_webhook_signature_with_nonce,
)
from sinch.domains.authentication.webhooks.v1.webhook_utils import (
    parse_json,
    normalize_iso_timestamp,
)
from sinch.domains.sms.webhooks.v1.events import (
    IncomingSMSWebhookEvent,
    MOTextWebhookEvent,
    MOBinaryWebhookEvent,
    MOMediaWebhookEvent,
)
from sinch.domains.sms.models.v1.response import (
    BatchDeliveryReport,
    RecipientDeliveryReport,
)


SmsCallback = Union[
    BatchDeliveryReport,
    RecipientDeliveryReport,
    MOTextWebhookEvent,
    MOBinaryWebhookEvent,
    MOMediaWebhookEvent,
]


class SmsWebhooks:
    def __init__(self, app_secret: Optional[str] = None):
        self.app_secret = app_secret

    def validate_authentication_header(
        self, headers: Dict[str, str], json_payload: str
    ) -> bool:
        """
        Validate the authorization header for a callback request.

        :param headers: Incoming request's headers
        :type headers: Dict[str, str]
        :param json_payload: Incoming request's raw body
        :type json_payload: str
        :returns: True if the X-Sinch-Webhook-Signature header is valid
        :rtype: bool
        """
        if not self.app_secret:
            return False
        return validate_webhook_signature_with_nonce(
            self.app_secret, headers, json_payload
        )

    def parse_event(
        self, event_body: Union[str, Dict[str, Any]]
    ) -> SmsCallback:
        """
        Parse the event payload into an SMS callback object.

        Handles datetime conversion for timestamp fields and routes to the
        appropriate event type based on the `type` field.

        :param event_body: The event payload (JSON string or dict).
        :type event_body: Union[str, Dict[str, Any]]
        :returns: A parsed SMS callback object.
        :rtype: SmsCallback
        :raises ValueError: If the event type is unknown or parsing fails.
        """
        if isinstance(event_body, str):
            event_body = parse_json(event_body)

        event_type = event_body.get("type")
        if not event_type:
            raise ValueError(f"Unknown SMS event: {json.dumps(event_body)}")

        # Handle delivery reports
        if event_type in ("delivery_report_sms", "delivery_report_mms"):
            return BatchDeliveryReport(**event_body)

        # Handle recipient delivery reports
        if event_type in (
            "recipient_delivery_report_sms",
            "recipient_delivery_report_mms",
        ):
            return RecipientDeliveryReport(**event_body)

        # Handle incoming SMS messages using discriminated union
        if event_type in ("mo_text", "mo_binary", "mo_media"):
            if "received_at" in event_body and isinstance(
                event_body["received_at"], str
            ):
                event_body["received_at"] = normalize_iso_timestamp(
                    event_body["received_at"]
                )
            if "sent_at" in event_body and isinstance(
                event_body["sent_at"], str
            ):
                event_body["sent_at"] = normalize_iso_timestamp(
                    event_body["sent_at"]
                )

            adapter = TypeAdapter(IncomingSMSWebhookEvent)
            return adapter.validate_python(event_body)

        raise ValueError(f"Unknown SMS event type: {event_type}")
