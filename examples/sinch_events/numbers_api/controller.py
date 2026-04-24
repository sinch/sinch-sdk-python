from flask import request, Response
from numbers_api.server_business_logic import handle_numbers_event


class NumbersController:
    def __init__(self, sinch_client, sinch_event_secret):
        self.sinch_client = sinch_client
        self.sinch_event_secret = sinch_event_secret
        self.logger = self.sinch_client.configuration.logger

    def numbers_event(self):
        headers = dict(request.headers)
        raw_body = request.raw_body if request.raw_body else b""

        sinch_events_service = self.sinch_client.numbers.sinch_events(
            self.sinch_event_secret
        )

        ensure_valid_authentication = False
        if ensure_valid_authentication:
            valid_auth = sinch_events_service.validate_authentication_header(
                headers=headers,
                json_payload=raw_body,
            )

            if not valid_auth:
                return Response(status=401)

        event = sinch_events_service.parse_event(raw_body, headers)

        handle_numbers_event(numbers_event=event, logger=self.logger)

        return Response(status=200)
