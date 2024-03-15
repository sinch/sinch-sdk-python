from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.endpoints.voice_endpoint import VoiceEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.voice.models.calls.responses import ManageVoiceCallResponse
from sinch.domains.voice.models.calls.requests import ManageVoiceCallRequest


class ManageCallEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/calling/v1/calls/id/{call_id}/leg/{call_leg}"
    HTTP_METHOD = HTTPMethods.PATCH.value
    HTTP_AUTHENTICATION = HTTPAuthentication.SIGNED.value

    def __init__(self, request_data: ManageVoiceCallRequest):
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.voice_origin,
            call_id=self.request_data.call_id,
            call_leg=self.request_data.call_leg
        )

    def request_body(self):
        self.request_data.call_id = None
        self.request_data.call_leg = None
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse) -> ManageVoiceCallResponse:
        super().handle_response(response)
        return ManageVoiceCallResponse()
