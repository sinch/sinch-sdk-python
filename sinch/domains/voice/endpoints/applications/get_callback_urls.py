from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.endpoints.voice_endpoint import VoiceEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.voice.models.applications.responses import GetCallbackUrlsVoiceApplicationResponse


class GetVoiceCallbacksEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/v1/configuration/callbacks/applications/{application_key}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.SIGNED.value

    def __init__(self):
        pass

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.voice_applications_origin,
            application_key=sinch.configuration.application_key
        )

    def handle_response(self, response: HTTPResponse) -> GetCallbackUrlsVoiceApplicationResponse:
        super().handle_response(response)
        return GetCallbackUrlsVoiceApplicationResponse(
            primary=response.body["url"]["primary"],
            fallback=response.body["url"]["fallback"]
        )
