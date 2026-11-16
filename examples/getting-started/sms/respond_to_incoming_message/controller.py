from flask import Response, jsonify, request
from server_business_logic import handle_sms_event

from sinch import SinchClient
from sinch.domains.sms.models.v1.shared import MOTextMessage
from sinch.domains.sms.sinch_events.v1 import SmsSinchEvent
from sinch.domains.sms.sinch_events.v1.events.sms_sinch_event import (
    SmsSinchEventPayload,
)


class SmsController:
    def __init__(self, sinch_client: SinchClient):
        self.sinch_client = sinch_client
        self.logger = self.sinch_client.configuration.logger

    def sms_event(self):
        raw_body = request.get_data()
        headers = dict(request.headers)

        try:
            event: SmsSinchEventPayload = SmsSinchEvent().parse_event(
                raw_body, headers
            )
            if isinstance(event, MOTextMessage):
                handle_sms_event(
                    event=event,
                    logger=self.logger,
                    sinch_client=self.sinch_client,
                )
            else:
                self.logger.info(f"Event of type: {event.type} received")
        except Exception as error:
            self.logger.error(
                "Unknown event or error parsing event: %s", error
            )
            return jsonify({"error": "Invalid event format"}), 400

        return Response(status=200)
