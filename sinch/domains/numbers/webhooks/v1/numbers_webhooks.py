from typing import Any, Dict, Union
from sinch.domains.authentication.webhooks.v1.authentication_validation import (
    validate_signature_header,
)
from sinch.domains.authentication.webhooks.v1.webhook_utils import (
    parse_json,
    normalize_iso_timestamp,
)
from sinch.domains.numbers.webhooks.v1.events import NumbersWebhooksEvent


class NumbersWebhooks:
    def __init__(self, callback_secret: str):
        self.callback_secret = callback_secret

    def validate_authentication_header(
        self, headers: Dict[str, str], json_payload: str
    ) -> bool:
        """
        Validate the authorization header for a callback request

        :param headers: Incoming request's headers
        :type headers: Dict[str, str]
        :param json_payload: Incoming request's raw body
        :type json_payload: str
        :returns: True if the X-Sinch-Signature header is valid
        :rtype: bool
        """
        return validate_signature_header(
            self.callback_secret, headers, json_payload
        )

    def parse_event(
        self, event_body: Union[str, Dict[str, Any]]
    ) -> NumbersWebhooksEvent:
        """
        Parses the event payload into a NumbersWebhooksEvent object.

        Handles a known issue where the server omits timezone information from
        the ``timestamp`` field. If the timezone is missing, the method assumes
        UTC and returns a timezone-aware ``datetime`` object.

        :param event_body: The event payload.
        :type event_body: Union[str, Dict[str, Any]]
        :returns: A parsed Pydantic object with a timezone-aware ``timestamp``.
        :rtype: NumbersWebhooksEvent
        """
        if isinstance(event_body, str):
            event_body = parse_json(event_body)
        timestamp = event_body.get("timestamp")
        if timestamp:
            event_body["timestamp"] = normalize_iso_timestamp(timestamp)
        try:
            return NumbersWebhooksEvent(**event_body)
        except Exception as e:
            raise ValueError(f"Failed to parse event body: {e}")
