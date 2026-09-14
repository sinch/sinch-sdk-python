from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.voice.api.v2.internal.base.voice_endpoint import (
    VoiceEndpoint,
)
from sinch.domains.voice.models.v2.calls.internal.request.start_call_request import (
    StartCallRequest,
)
from sinch.domains.voice.models.v2.calls.response.start_call_response import (
    StartCallResponse,
)


class StartCallEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/calls"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS = {"service_id"}
    HEADER_PARAM_FIELDS = {"idempotency_key"}

    def __init__(
        self,
        project_id: str,
        request_data: StartCallRequest,
        response_model=StartCallResponse,
    ):
        super().__init__(project_id, request_data, response_model)
