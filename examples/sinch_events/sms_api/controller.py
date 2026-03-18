from flask import request, Response
from sinch_events.sms_api.server_business_logic import (
    handle_sms_event,
)


class SmsController:
    def __init__(self, sinch_client, webhooks_secret):
        self.sinch_client = sinch_client
        self.webhooks_secret = webhooks_secret
        self.logger = self.sinch_client.configuration.logger

    def sms_event(self):
        headers = dict(request.headers)
        raw_body = request.raw_body if request.raw_body else b""

        webhooks_service = self.sinch_client.sms.sinch_events(self.webhooks_secret)

        # Signature headers may be absent unless your account manager enables them
        # (see README: Configuration -> Controller Settings -> SMS controller);
        # leave auth disabled here unless SMS callbacks are configured.
        ensure_valid_authentication = False
        if ensure_valid_authentication:
            valid_auth = webhooks_service.validate_authentication_header(
                headers=headers,
                json_payload=raw_body,
            )

            if not valid_auth:
                return Response(status=401)

        event = webhooks_service.parse_event(raw_body, headers)

        handle_sms_event(sms_event=event, logger=self.logger)

        return Response(status=200)
