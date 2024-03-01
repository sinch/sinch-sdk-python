from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.endpoints.voice_endpoint import VoiceEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.voice.models.applications.requests import AssignNumbersVoiceApplicationRequest
from sinch.domains.voice.models.applications.responses import AssignNumbersVoiceApplicationResponse


class AssignVoiceNumbersEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/v1/configuration/numbers"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.SIGNED.value

    def __init__(self, request_data: AssignNumbersVoiceApplicationRequest):
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.voice_applications_origin
        )

    def request_body(self):
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse) -> AssignNumbersVoiceApplicationResponse:
        super().handle_response(response)
        return AssignNumbersVoiceApplicationResponse()
