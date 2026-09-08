from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.voice.api.v2.internal.base.voice_endpoint import (
    VoiceEndpoint,
)
from sinch.domains.voice.models.v2.batches.internal.request.batch_id_request import (
    BatchIdRequest,
)
from sinch.domains.voice.models.v2.batches.response.batch_details_response import (
    BatchDetailsResponse,
)
from sinch.domains.voice.models.v2.batches.response.batch_summary_response import (
    BatchSummaryResponse,
)


class GetBatchCallSummaryEndpoint(VoiceEndpoint):
    UNSET_SERIALIZATION = True
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
    UNSET_SERIALIZATION = True
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
    UNSET_SERIALIZATION = True
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
