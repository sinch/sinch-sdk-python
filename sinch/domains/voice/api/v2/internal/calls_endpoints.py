from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.voice.api.v2.internal.base.voice_endpoint import (
    VoiceEndpoint,
)
from sinch.domains.voice.models.v2.calls.internal.list_calls_response import (
    ListCallsResponse,
)
from sinch.domains.voice.models.v2.calls.internal.request.call_id_request import (
    CallIdRequest,
)
from sinch.domains.voice.models.v2.calls.internal.request.list_calls_request import (
    ListCallsRequest,
)
from sinch.domains.voice.models.v2.calls.internal.request.patch_call_by_id_request import (
    PatchCallByIdRequest,
)
from sinch.domains.voice.models.v2.calls.internal.request.patch_call_by_session_and_name_request import (
    PatchCallBySessionAndNameRequest,
)
from sinch.domains.voice.models.v2.calls.internal.request.start_call_request import (
    StartCallRequest,
)
from sinch.domains.voice.models.v2.calls.response.start_call_response import (
    StartCallResponse,
)
from sinch.domains.voice.models.v2.shared.call import Call


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


class ListCallsEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/calls"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS = {
        "service_id",
        "from_",
        "to",
        "call_type",
        "start_time",
        "end_time",
        "call_result",
        "call_reason",
        "page_size",
        "page",
    }

    def __init__(
        self,
        project_id: str,
        request_data: ListCallsRequest,
        response_model=ListCallsResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class GetCallByIdEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/calls/{call_id}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: CallIdRequest,
        response_model=Call,
    ):
        super().__init__(project_id, request_data, response_model)


class PatchCallByIdEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/calls/{call_id}"
    HTTP_METHOD = HTTPMethods.PATCH.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    HEADER_PARAM_FIELDS = {"idempotency_key"}

    def __init__(
        self,
        project_id: str,
        request_data: PatchCallByIdRequest,
        response_model=None,
    ):
        super().__init__(project_id, request_data, response_model)


class PatchCallBySessionAndNameEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/sessions/{session_id}/calls/{call_name}"
    HTTP_METHOD = HTTPMethods.PATCH.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    HEADER_PARAM_FIELDS = {"idempotency_key"}

    def __init__(
        self,
        project_id: str,
        request_data: PatchCallBySessionAndNameRequest,
        response_model=None,
    ):
        super().__init__(project_id, request_data, response_model)
