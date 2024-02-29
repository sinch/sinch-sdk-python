from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.endpoints.voice_endpoint import VoiceEndpoint
from sinch.domains.voice.models import ApplicationNumber
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.voice.models.applications.responses import GetNumbersVoiceApplicationResponse


class GetVoiceNumbersEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/v1/configuration/numbers"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.SIGNED.value

    def __init__(self):
        pass

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.voice_applications_origin
        )

    def handle_response(self, response: HTTPResponse) -> GetNumbersVoiceApplicationResponse:
        super().handle_response(response)
        return GetNumbersVoiceApplicationResponse(
            numbers=[
                ApplicationNumber(
                    number=number["number"],
                    capability=number["capability"]
                ) for number in response.body["numbers"]
            ]
        )
