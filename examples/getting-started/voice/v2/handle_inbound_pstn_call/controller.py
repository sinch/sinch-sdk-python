from config import config
from flask import Response, jsonify, request
from server_business_logic import handle_voice_event

from sinch import SinchClient

class VoiceController:
    def __init__(self, sinch_client: SinchClient):
        self.sinch_client = sinch_client
        self.logger = self.sinch_client.configuration.logger

    def voice_event(self):
        headers = dict(request.headers)
        raw_body = request.get_data()
        path = request.path
        method = request.method
        service_id = config.get("SINCH_SERVICE_ID", "")
        service_secret = config.get("SINCH_SERVICE_SECRET", "")
        sinch_number = config.get("SINCH_NUMBER", "")
        destination_number = config.get("DESTINATION_NUMBER", "")

        sinch_events_service = self.sinch_client.voice.v2.sinch_events

        is_valid_request: bool = (
            sinch_events_service.validate_authentication_header(
                method=method,
                path=path,
                headers=headers,
                body=raw_body,
                service_id=service_id,
                service_secret=service_secret,
            )
        )

        if not is_valid_request:
            self.logger.warning("Request is not valid")
            return Response(status=401)

        voice_event_request = sinch_events_service.parse_event(
            raw_body, headers
        )
        voice_event_response = handle_voice_event(
            event=voice_event_request,
            logger=self.logger,
            sinch_events_service=sinch_events_service,
            sinch_number=sinch_number,
            destination_number=destination_number,
        )

        return jsonify(sinch_events_service.serialize_response(voice_event_response)), 200
