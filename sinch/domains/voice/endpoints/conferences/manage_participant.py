from copy import deepcopy
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.endpoints.voice_endpoint import VoiceEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.voice.models.conferences.responses import ManageParticipantVoiceConferenceResponse
from sinch.domains.voice.models.conferences.requests import ManageParticipantVoiceConferenceRequest


class ManageParticipantConferenceEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/calling/v1/conferences/id/{conference_id}/{call_id}"
    HTTP_METHOD = HTTPMethods.PATCH.value
    HTTP_AUTHENTICATION = HTTPAuthentication.SIGNED.value

    def __init__(self, request_data: ManageParticipantVoiceConferenceRequest):
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.voice_origin,
            conference_id=self.request_data.conference_id,
            call_id=self.request_data.call_id
        )

    def request_body(self):
        request_data = deepcopy(self.request_data)
        request_data.conference_id = None
        request_data.call_id = None
        return request_data.as_json()

    def handle_response(self, response: HTTPResponse) -> ManageParticipantVoiceConferenceResponse:
        super().handle_response(response)
        return ManageParticipantVoiceConferenceResponse()
