import json
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.models.v1.internal import (
    BatchIdRequest,
    DryRunRequest,
    ListBatchesRequest,
    ReplaceBatchRequest,
    SendSMSRequest,
    DeliveryFeedbackRequest,
    UpdateBatchMessageRequest,
)
from sinch.domains.sms.models.v1.response.list_batches_response import (
    ListBatchesResponse,
)
from sinch.domains.sms.models.v1.types import BatchResponse
from sinch.domains.sms.models.v1.response.dry_run_response import (
    DryRunResponse,
)
from sinch.domains.sms.api.v1.internal.base import SmsEndpoint
from sinch.domains.sms.api.v1.exceptions import SmsException


class CancelBatchMessageEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/batches/{batch_id}"
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: BatchIdRequest):
        super(CancelBatchMessageEndpoint, self).__init__(
            project_id, request_data
        )
        self.project_id = project_id
        self.request_data = request_data

    def handle_response(self, response: HTTPResponse) -> BatchResponse:
        try:
            super(CancelBatchMessageEndpoint, self).handle_response(response)
        except SmsException as e:
            raise SmsException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(response.body, BatchResponse)


class DryRunEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/batches/dry_run"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    # Define which fields are query parameters (not part of the request body)
    QUERY_PARAM_FIELDS = {"per_recipient", "number_of_recipients"}

    def __init__(self, project_id: str, request_data: DryRunRequest):
        super(DryRunEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_query_params(self) -> dict:
        """Extract query parameters from request data."""
        # Extract only query param fields using include, and exclude None values
        query_params = self.request_data.model_dump(
            include=self.QUERY_PARAM_FIELDS, exclude_none=True, by_alias=True
        )
        return query_params

    def request_body(self):
        """Extract body (excluding query params) and serialize datetime to JSON."""
        # Exclude query params from body using the same constant
        # Use mode='json' to serialize datetime objects to ISO-8601 strings
        request_data = self.request_data.model_dump(
            mode="json",
            by_alias=True,
            exclude_none=True,
            exclude=self.QUERY_PARAM_FIELDS,
        )
        return json.dumps(request_data)

    def handle_response(self, response: HTTPResponse) -> DryRunResponse:
        try:
            super(DryRunEndpoint, self).handle_response(response)
        except SmsException as e:
            raise SmsException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(response.body, DryRunResponse)


class GetBatchMessageEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/batches/{batch_id}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: BatchIdRequest):
        super(GetBatchMessageEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def handle_response(self, response: HTTPResponse) -> BatchResponse:
        try:
            super(GetBatchMessageEndpoint, self).handle_response(response)
        except SmsException as e:
            raise SmsException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(response.body, BatchResponse)


class ListBatchesEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/batches"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: ListBatchesRequest):
        super(ListBatchesEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_query_params(self) -> dict:
        return self.request_data.model_dump(exclude_none=True, by_alias=True)

    def handle_response(self, response: HTTPResponse) -> ListBatchesResponse:
        try:
            super(ListBatchesEndpoint, self).handle_response(response)
        except SmsException as e:
            raise SmsException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(response.body, ListBatchesResponse)


class ReplaceBatchEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/batches/{batch_id}"
    HTTP_METHOD = HTTPMethods.PUT.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: ReplaceBatchRequest):
        super(ReplaceBatchEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def request_body(self):
        # Used mode='json' to serialize datetime objects to ISO-8601 strings
        # Exclude batch_id from body since it's in the URL path
        request_data = self.request_data.model_dump(
            mode="json", by_alias=True, exclude_none=True, exclude={"batch_id"}
        )
        return json.dumps(request_data)

    def handle_response(self, response: HTTPResponse) -> BatchResponse:
        try:
            super(ReplaceBatchEndpoint, self).handle_response(response)
        except SmsException as e:
            raise SmsException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(response.body, BatchResponse)


class SendSMSEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/batches"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: SendSMSRequest):
        super(SendSMSEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def request_body(self):
        # Use mode='json' to serialize datetime objects to ISO-8601 strings
        request_data = self.request_data.model_dump(
            mode="json", by_alias=True, exclude_none=True
        )
        return json.dumps(request_data)

    def handle_response(self, response: HTTPResponse) -> BatchResponse:
        try:
            super(SendSMSEndpoint, self).handle_response(response)
        except SmsException as e:
            raise SmsException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(response.body, BatchResponse)


class DeliveryFeedbackEndpoint(SmsEndpoint):
    ENDPOINT_URL = (
        "{origin}/xms/v1/{project_id}/batches/{batch_id}/delivery_feedback"
    )
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: DeliveryFeedbackRequest):
        super(DeliveryFeedbackEndpoint, self).__init__(
            project_id, request_data
        )
        self.project_id = project_id
        self.request_data = request_data

    def request_body(self):
        request_data = self.request_data.model_dump(
            by_alias=True, exclude_none=True
        )
        return json.dumps(request_data)

    def handle_response(self, response: HTTPResponse):
        try:
            super(DeliveryFeedbackEndpoint, self).handle_response(response)
        except SmsException as e:
            raise SmsException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )


class UpdateBatchMessageEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/batches/{batch_id}"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self, project_id: str, request_data: UpdateBatchMessageRequest
    ):
        super(UpdateBatchMessageEndpoint, self).__init__(
            project_id, request_data
        )
        self.project_id = project_id
        self.request_data = request_data

    def request_body(self):
        # Use mode='json' to serialize datetime objects to ISO-8601 strings
        # Exclude batch_id from body since it's in the URL path
        request_data = self.request_data.model_dump(
            mode="json", by_alias=True, exclude_none=True, exclude={"batch_id"}
        )
        return json.dumps(request_data)

    def handle_response(self, response: HTTPResponse) -> BatchResponse:
        try:
            super(UpdateBatchMessageEndpoint, self).handle_response(response)
        except SmsException as e:
            raise SmsException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(response.body, BatchResponse)
