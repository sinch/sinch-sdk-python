from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.endpoints.voice_endpoint import VoiceEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.voice.models.conferences.responses import KickParticipantVoiceConferenceResponse
from sinch.domains.voice.models.conferences.requests import KickParticipantVoiceConferenceRequest


class KickParticipantConferenceEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/calling/v1/conferences/id/{conference_id}/{call_id}"
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.SIGNED.value

    def __init__(self, request_data: KickParticipantVoiceConferenceRequest):
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.voice_origin,
            conference_id=self.request_data.conference_id,
            call_id=self.request_data.call_id
        )

    def handle_response(self, response: HTTPResponse) -> KickParticipantVoiceConferenceResponse:
        super().handle_response(response)
        return KickParticipantVoiceConferenceResponse()
