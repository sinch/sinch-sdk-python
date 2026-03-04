from flask import request, Response
from server_business_logic import handle_conversation_event


class ConversationController:
    def __init__(self, sinch_client, webhooks_secret, app_id):
        self.sinch_client = sinch_client
        self.webhooks_secret = webhooks_secret
        self.app_id = app_id
        self.logger = self.sinch_client.configuration.logger

    def conversation_event(self):
        headers = dict(request.headers)
        raw_body = getattr(request, "raw_body", None) or b""

        webhooks_service = self.sinch_client.conversation.webhooks(self.webhooks_secret)

        valid = webhooks_service.validate_authentication_header(
            headers=headers,
            json_payload=raw_body,
        )
        if not valid:
            return Response(status=401)

        event = webhooks_service.parse_event(raw_body, headers)
        handle_conversation_event(
            event=event,
            logger=self.logger,
            sinch_client=self.sinch_client,
            app_id=self.app_id,
        )

        return Response(status=200)
