from typing import Any, Dict, Optional, Union
from sinch.domains.authentication.webhooks.v1.authentication_validation import (
    validate_signature_header,
)
from sinch.domains.authentication.webhooks.v1.webhook_utils import (
    decode_payload,
    parse_json,
    normalize_iso_timestamp,
)
from sinch.domains.numbers.sinch_events.v1.events import NumberSinchEvent


class SinchEvents:
    def __init__(self, callback_secret: str):
        self.callback_secret = callback_secret

    def validate_authentication_header(
        self,
        headers: Dict[str, str],
        json_payload: Union[str, bytes],
    ) -> bool:
        """
        Validate the authorization header for a callback request

        :param headers: Incoming request's headers
        :type headers: Dict[str, str]
        :param json_payload: Incoming request's raw body (str or bytes)
        :type json_payload: Union[str, bytes]
        :returns: True if the X-Sinch-Signature header is valid
        :rtype: bool
        """
        payload_str = (
            decode_payload(json_payload, headers)
            if isinstance(json_payload, bytes)
            else json_payload
        )
        return validate_signature_header(
            self.callback_secret, headers, payload_str
        )

    def parse_event(
        self,
        event_body: Union[str, bytes, Dict[str, Any]],
        headers: Optional[Dict[str, str]] = None,
    ) -> NumberSinchEvent:
        """
        Parses the event payload into a NumberSinchEvent object.

        Handles a known issue where the server omits timezone information from
        the ``timestamp`` field. If the timezone is missing, the method assumes
        UTC and returns a timezone-aware ``datetime`` object.

        :param event_body: The event payload (JSON string, raw bytes, or dict).
        :type event_body: Union[str, bytes, Dict[str, Any]]
        :param headers: Request headers (used to decode charset when event_body is bytes).
        :type headers: Optional[Dict[str, str]]
        :returns: A parsed Pydantic object with a timezone-aware ``timestamp``.
        :rtype: NumberSinchEvent
        """
        if isinstance(event_body, bytes):
            event_body = parse_json(decode_payload(event_body, headers))
        elif isinstance(event_body, str):
            event_body = parse_json(event_body)
        timestamp = event_body.get("timestamp")
        if timestamp:
            event_body["timestamp"] = normalize_iso_timestamp(timestamp)
        try:
            return NumberSinchEvent(**event_body)
        except Exception as e:
            raise ValueError(f"Failed to parse event body: {e}")
