from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.endpoints.voice_endpoint import VoiceEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.voice.models.calls.responses import UpdateVoiceCallResponse
from sinch.domains.voice.models.calls.requests import UpdateVoiceCallRequest


class UpdateCallEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/calling/v1/calls/id/{call_id}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.SIGNED.value

    def __init__(self, request_data: UpdateVoiceCallRequest):
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.voice_origin,
            call_id=self.request_data.callId
        )

    def request_body(self):
        self.request_data.callId = None
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse) -> UpdateVoiceCallResponse:
        super().handle_response(response)
        return UpdateVoiceCallResponse()
