from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.sms.api.v1.internal.base import SmsEndpoint
from sinch.domains.sms.models.v1.internal import (
    BatchIdRequest,
    DeliveryFeedbackRequest,
    ListBatchesRequest,
)
from sinch.domains.sms.models.v1.internal.dry_run_request import DryRunRequest
from sinch.domains.sms.models.v1.internal.replace_batch_request import (
    ReplaceBatchRequest,
)
from sinch.domains.sms.models.v1.internal.send_sms_request import (
    SendSMSRequest,
)
from sinch.domains.sms.models.v1.internal.update_batch_message_request import (
    UpdateBatchMessageRequest,
)
from sinch.domains.sms.models.v1.response.dry_run_response import (
    DryRunResponse,
)
from sinch.domains.sms.models.v1.response.list_batches_response import (
    ListBatchesResponse,
)
from sinch.domains.sms.models.v1.types.batch_response import BatchResponse


class CancelBatchMessageEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/batches/{batch_id}"
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: BatchIdRequest,
        response_model=BatchResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class DryRunEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/batches/dry_run"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    # Define which fields are query parameters (not part of the request body)
    QUERY_PARAM_FIELDS = {"per_recipient", "number_of_recipients"}

    def __init__(
        self,
        project_id: str,
        request_data: DryRunRequest,
        response_model=DryRunResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class GetBatchMessageEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/batches/{batch_id}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: BatchIdRequest,
        response_model=BatchResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class ListBatchesEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/batches"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS: set = {
        "page",
        "page_size",
        "start_date",
        "end_date",
        "client_reference",
    }
    QUERY_PARAM_FIELDS_EXPLODE_FALSE: set = {"from_"}

    def __init__(
        self,
        project_id: str,
        request_data: ListBatchesRequest,
        response_model=ListBatchesResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class ReplaceBatchEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/batches/{batch_id}"
    HTTP_METHOD = HTTPMethods.PUT.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: ReplaceBatchRequest,
        response_model=BatchResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class SendSMSEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/batches"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: SendSMSRequest,
        response_model=BatchResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class DeliveryFeedbackEndpoint(SmsEndpoint):
    ENDPOINT_URL = (
        "{origin}/xms/v1/{project_id}/batches/{batch_id}/delivery_feedback"
    )
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: DeliveryFeedbackRequest):
        super().__init__(project_id, request_data)


class UpdateBatchMessageEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/batches/{batch_id}"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: UpdateBatchMessageRequest,
        response_model=BatchResponse,
    ):
        super().__init__(project_id, request_data, response_model)
