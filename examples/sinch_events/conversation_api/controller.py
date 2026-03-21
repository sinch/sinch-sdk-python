from flask import request, Response
from sinch_events.conversation_api.server_business_logic import handle_conversation_event


class ConversationController:
    def __init__(self, sinch_client, sinch_event_secret):
        self.sinch_client = sinch_client
        self.sinch_event_secret = sinch_event_secret
        self.logger = self.sinch_client.configuration.logger

    def conversation_event(self):
        headers = dict(request.headers)
        raw_body = request.raw_body if request.raw_body else b""

        sinch_events_service = self.sinch_client.conversation.sinch_events(
            self.sinch_event_secret
        )

        # Set to True to enforce signature validation (recommended in production)
        ensure_valid_signature = False
        if ensure_valid_signature:
            valid = sinch_events_service.validate_authentication_header(
                headers=headers,
                json_payload=raw_body,
            )
            if not valid:
                return Response(status=401)

        event = sinch_events_service.parse_event(raw_body, headers)
        handle_conversation_event(event=event, logger=self.logger)

        return Response(status=200)
