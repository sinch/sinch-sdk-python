from flask import request, Response
from webhooks.sms_api.server_business_logic import (
    handle_sms_event,
)


class SmsController:
    def __init__(self, sinch_client, webhooks_secret=None):
        self.sinch_client = sinch_client
        self.webhooks_secret = webhooks_secret
        self.logger = self.sinch_client.configuration.logger

    def sms_event(self):
        body_str = request.raw_body.decode('utf-8') if request.raw_body else ''

        webhooks_service = self.sinch_client.sms.webhooks(self.webhooks_secret)

        event = webhooks_service.parse_event(body_str)

        event_type = getattr(event, 'type', None)

        self.logger.info(f'Handling SMS event: {event_type}')

        handle_sms_event(sms_event=event, logger=self.logger)

        return Response(status=200)
