from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.endpoints.voice_endpoint import VoiceEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.voice.models.applications.responses import GetCallbackUrlsVoiceApplicationResponse
from sinch.domains.voice.models.applications.requests import GetCallbackUrlsVoiceApplicationRequest


class GetVoiceCallbacksEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/v1/configuration/callbacks/applications/{application_key}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.SIGNED.value

    def __init__(self, request_data: GetCallbackUrlsVoiceApplicationRequest):
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.voice_applications_origin, application_key=self.request_data.application_key
        )

    def handle_response(self, response: HTTPResponse) -> GetCallbackUrlsVoiceApplicationResponse:
        super().handle_response(response)
        return GetCallbackUrlsVoiceApplicationResponse(
            primary=response.body["url"].get("primary"), fallback=response.body["url"].get("fallback")
        )
