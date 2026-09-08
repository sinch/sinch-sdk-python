from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.voice.api.v2.internal.base.voice_endpoint import (
    VoiceEndpoint,
)
from sinch.domains.voice.models.v2.sessions.internal.request.session_id_request import (
    SessionIdRequest,
)
from sinch.domains.voice.models.v2.sessions.response.session_response import (
    SessionResponse,
)


class GetSessionEndpoint(VoiceEndpoint):
    UNSET_SERIALIZATION = True
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/sessions/{session_id}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: SessionIdRequest,
        response_model=SessionResponse,
    ):
        super().__init__(project_id, request_data, response_model)
