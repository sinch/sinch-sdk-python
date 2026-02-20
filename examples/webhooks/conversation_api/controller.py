import re
from flask import request, Response
from webhooks.conversation_api.server_business_logic import handle_conversation_event


def _charset_from_content_type(content_type):
    """Extract charset from Content-Type header; default to utf-8 if missing."""
    if not content_type:
        return "utf-8"
    match = re.search(r"charset\s*=\s*([^\s;]+)", content_type, re.I)
    return match.group(1).strip("'\"").lower() if match else "utf-8"


def _decode_body(raw_body, content_type):
    """Decode request body using Content-Type charset, fallback to utf-8."""
    if not raw_body:
        return ""
    charset = _charset_from_content_type(content_type)
    try:
        return raw_body.decode(charset)
    except (LookupError, UnicodeDecodeError):
        return raw_body.decode("utf-8")


class ConversationController:
    def __init__(self, sinch_client, webhooks_secret):
        self.sinch_client = sinch_client
        self.webhooks_secret = webhooks_secret
        self.logger = self.sinch_client.configuration.logger

    def conversation_event(self):
        headers = dict(request.headers)
        raw_body = request.raw_body if request.raw_body else b""
        content_type = headers.get("Content-Type") or headers.get("content-type") or ""
        body_str = _decode_body(raw_body, content_type)

        webhooks_service = self.sinch_client.conversation.webhooks(self.webhooks_secret)

        # Set to True to enforce signature validation (recommended in production)
        ensure_valid_signature = False
        if ensure_valid_signature:
            valid = webhooks_service.validate_authentication_header(
                headers=headers,
                json_payload=body_str,
            )
            if not valid:
                return Response(status=401)

        event = webhooks_service.parse_event(body_str)
        handle_conversation_event(event=event, logger=self.logger)

        return Response(status=200)
