from flask import request, Response
from server_business_logic import handle_conversation_event


class ConversationController:
    def __init__(self, sinch_client):
        self.sinch_client = sinch_client
        self.logger = self.sinch_client.configuration.logger

    def conversation_event(self):
        headers = dict(request.headers)
        raw_body = getattr(request, "raw_body", None) or b""

        sinch_events_service = self.sinch_client.conversation.sinch_events()
        event = sinch_events_service.parse_event(raw_body, headers)
        handle_conversation_event(
            event=event,
            logger=self.logger,
            sinch_client=self.sinch_client,
        )

        return Response(status=200)
