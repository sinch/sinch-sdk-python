from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.endpoints.voice_endpoint import VoiceEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.voice.models.applications.requests import UnassignNumbersVoiceApplicationRequest
from sinch.domains.voice.models.applications.responses import UnassignNumbersVoiceApplicationResponse


class UnAssignVoiceNumberEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/v1/configuration/numbers"
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.SIGNED.value

    def __init__(self, request_data: UnassignNumbersVoiceApplicationRequest):
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.voice_applications_origin,
            number=self.request_data.number
        )

    def handle_response(self, response: HTTPResponse) -> UnassignNumbersVoiceApplicationResponse:
        super().handle_response(response)
        return UnassignNumbersVoiceApplicationResponse()
