import json
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.endpoints.voice_endpoint import VoiceEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.voice.models.applications.requests import UpdateCallbackUrlsVoiceApplicationRequest
from sinch.domains.voice.models.applications.responses import UpdateCallbackUrlsVoiceApplicationResponse


class UpdateVoiceCallbacksEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/v1/configuration/callbacks/applications/{application_key}"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.SIGNED.value

    def __init__(self, request_data: UpdateCallbackUrlsVoiceApplicationRequest):
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.voice_applications_origin, application_key=self.request_data.application_key
        )

    def request_body(self):
        request_data = {"url": {}}

        if self.request_data.primary:
            request_data["url"]["primary"] = self.request_data.primary

        if self.request_data.primary:
            request_data["url"]["fallback"] = self.request_data.fallback

        return json.dumps(request_data)

    def handle_response(self, response: HTTPResponse) -> UpdateCallbackUrlsVoiceApplicationResponse:
        super().handle_response(response)
        return UpdateCallbackUrlsVoiceApplicationResponse()
