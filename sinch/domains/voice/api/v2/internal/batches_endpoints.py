from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.voice.api.v2.internal.base.voice_endpoint import (
    VoiceEndpoint,
)
from sinch.domains.voice.models.v2.batches.internal.request.batch_id_request import (
    BatchIdRequest,
)
from sinch.domains.voice.models.v2.batches.internal.request.start_batch_request import (
    StartBatchRequest,
)
from sinch.domains.voice.models.v2.batches.response.batch_details_response import (
    BatchDetailsResponse,
)
from sinch.domains.voice.models.v2.batches.response.batch_summary_response import (
    BatchSummaryResponse,
)
from sinch.domains.voice.models.v2.batches.response.start_batch_response import (
    StartBatchResponse,
)


class StartBatchEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/calls"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS = {"service_id"}
    HEADER_PARAM_FIELDS = {"idempotency_key"}

    def __init__(
        self,
        project_id: str,
        request_data: StartBatchRequest,
        response_model=StartBatchResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class GetBatchCallSummaryEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/batches/{batch_id}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: BatchIdRequest,
        response_model=BatchSummaryResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class StopBatchProcessingEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/batches/{batch_id}"
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: BatchIdRequest,
        response_model=None,
    ):
        super().__init__(project_id, request_data, response_model)


class GetBatchDetailsEndpoint(VoiceEndpoint):
    ENDPOINT_URL = (
        "{origin}/v2/projects/{project_id}/batches/{batch_id}/details"
    )
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: BatchIdRequest,
        response_model=BatchDetailsResponse,
    ):
        super().__init__(project_id, request_data, response_model)
