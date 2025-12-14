from flask import request, Response
from webhooks.numbers_api.server_business_logic import handle_numbers_event


class NumbersController:
    def __init__(self, sinch_client, webhooks_secret):
        self.sinch_client = sinch_client
        self.webhooks_secret = webhooks_secret
        self.logger = self.sinch_client.configuration.logger

    def numbers_event(self):
        headers = dict(request.headers)
        body_str = request.raw_body.decode('utf-8') if request.raw_body else ''

        webhooks_service = self.sinch_client.numbers.webhooks(self.webhooks_secret)

        valid_auth = webhooks_service.validate_authentication_header(
            headers=headers,
            json_payload=body_str
        )

        if not valid_auth:
            self.logger.error('Invalid authentication header')
            return Response(status=401)

        event = webhooks_service.parse_event(body_str)

        handle_numbers_event(numbers_event=event, logger=self.logger)

        return Response(status=200)
