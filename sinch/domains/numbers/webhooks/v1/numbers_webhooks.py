import json
from typing import Any, Dict, Union
from datetime import datetime
import re
from pydantic import StrictBool, StrictStr
from sinch.domains.authentication.webhooks.v1.authentication_validation import validate_signature_header
from sinch.domains.numbers.webhooks.v1.events import NumbersWebhooksEvent


class NumbersWebhooks:
    def __init__(self, callback_secret: StrictStr):
        self.callback_secret = callback_secret

    def validate_authentication_header(
        self,
        headers: Dict[StrictStr, StrictStr],
        json_payload: StrictStr
    ) -> StrictBool:
        """
        Validate the authorization header for a callback request

        :param headers: Incoming request's headers
        :type headers: Dict[str, str]
        :param json_payload: Incoming request's raw body
        :type json_payload: StrictStr
        :returns: True if the X-Sinch-Signature header is valid
        :rtype: bool
        """
        return validate_signature_header(
            self.callback_secret,
            headers,
            json_payload
        )

    def parse_event(self, event_body: Union[StrictStr, Dict[StrictStr, Any]]) -> NumbersWebhooksEvent:
        """
        Parses the event payload into a NumbersWebhooksEvent object.

        Handles a known issue where the server omits timezone information from
        the ``timestamp`` field. If the timezone is missing, the method assumes
        UTC and returns a timezone-aware ``datetime`` object.

        :param event_body: The event payload.
        :type event_body: Union[StrictStr, Dict[StrictStr, Any]]
        :returns: A parsed Pydantic object with a timezone-aware ``timestamp``.
        :rtype: NumbersWebhooksEvent
        """
        if isinstance(event_body, str):
            event_body = self._parse_json(event_body)
        timestamp = event_body.get('timestamp')
        if timestamp:
            event_body["timestamp"] = self._normalize_iso_timestamp(timestamp)
        try:
            return NumbersWebhooksEvent(**event_body)
        except Exception as e:
            raise ValueError(f"Failed to parse event body: {e}")

    def _parse_json(self, payload: StrictStr) -> Dict[StrictStr, Any]:
        """
        Parse JSON string into a dictionary.
        """
        try:
            return json.loads(payload)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON: {e}")

    def _normalize_iso_timestamp(self, timestamp: StrictStr) -> datetime:
        """
        Normalize a timestamp string to ensure compatibility with Python's `datetime.fromisoformat()`
        - Ensures that the timestamp includes a UTC offset (e.g., "+00:00") if missing.
        - Replaces trailing "Z" with "+00:00" to indicate UTC.
        - Trims microseconds to 6 digits.
        """
        if timestamp.endswith("Z"):
            timestamp = timestamp.replace("Z", "+00:00")
        elif not re.search(r"(Z|[+-]\d{2}:?\d{2})$", timestamp):
            timestamp += "+00:00"
        match_ms = re.search(r"\.(\d{7,})(?=[+-])", timestamp)
        if match_ms:
            micro_trimmed = match_ms.group(1)[:6]
            timestamp = re.sub(r"\.\d{7,}(?=[+-])", f".{micro_trimmed}", timestamp)
        try:
            return datetime.fromisoformat(timestamp)
        except ValueError as e:
            raise ValueError(f"Invalid timestamp format: {e}")
