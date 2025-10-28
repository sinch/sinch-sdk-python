from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.http_response import HTTPResponse
from sinch.core.models.utils import model_dump_for_query_params
from sinch.domains.sms.api.v1.exceptions import SmsException
from sinch.domains.sms.models.v1.internal import (
    GetBatchDeliveryReportRequest,
    GetRecipientDeliveryReportRequest,
    ListDeliveryReportsRequest,
    ListDeliveryReportsResponse,
)
from sinch.domains.sms.api.v1.internal.base import SmsEndpoint
from sinch.domains.sms.models.v1.response import (
    BatchDeliveryReport,
    RecipientDeliveryReport,
)


class GetBatchDeliveryReportEndpoint(SmsEndpoint):
    ENDPOINT_URL = (
        "{origin}/xms/v1/{project_id}/batches/{batch_id}/delivery_report"
    )
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self, project_id: str, request_data: GetBatchDeliveryReportRequest
    ):
        super(GetBatchDeliveryReportEndpoint, self).__init__(
            project_id, request_data
        )
        self.project_id = project_id
        self.request_data = request_data

    def build_query_params(self) -> dict:
        return model_dump_for_query_params(self.request_data)

    def handle_response(self, response: HTTPResponse) -> BatchDeliveryReport:
        try:
            super(GetBatchDeliveryReportEndpoint, self).handle_response(
                response
            )
        except SmsException as e:
            raise SmsException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(response.body, BatchDeliveryReport)


class GetRecipientDeliveryReportEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/batches/{batch_id}/delivery_report/{recipient_msisdn}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: GetRecipientDeliveryReportRequest,
    ):
        super(GetRecipientDeliveryReportEndpoint, self).__init__(
            project_id, request_data
        )
        self.project_id = project_id
        self.request_data = request_data

    def handle_response(
        self, response: HTTPResponse
    ) -> RecipientDeliveryReport:
        try:
            super(GetRecipientDeliveryReportEndpoint, self).handle_response(
                response
            )
        except SmsException as e:
            raise SmsException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(
            response.body, RecipientDeliveryReport
        )


class ListDeliveryReportsEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/delivery_reports"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self, project_id: str, request_data: ListDeliveryReportsRequest
    ):
        super(ListDeliveryReportsEndpoint, self).__init__(
            project_id, request_data
        )
        self.project_id = project_id
        self.request_data = request_data

    def build_query_params(self) -> dict:
        return model_dump_for_query_params(self.request_data)

    def handle_response(
        self, response: HTTPResponse
    ) -> ListDeliveryReportsResponse:
        try:
            super(ListDeliveryReportsEndpoint, self).handle_response(response)
        except SmsException as e:
            raise SmsException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(
            response.body, ListDeliveryReportsResponse
        )
