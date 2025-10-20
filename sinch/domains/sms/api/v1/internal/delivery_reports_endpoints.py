from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.api.v1.exceptions import SmsException
from sinch.domains.sms.models.v1.internal import (
    GetDeliveryReportsByBatchIdRequest,
    GetDeliveryReportsByPhoneNumberRequest,
    ListDeliveryReportsRequest,
    ListDeliveryReportsResponse,
)
from sinch.domains.sms.api.v1.internal.base import SmsEndpoint
from sinch.domains.sms.models.v1.response import (
    BatchDeliveryReport,
    RecipientDeliveryReport,
)


class GetDeliveryReportByBatchIdEndpoint(SmsEndpoint):
    ENDPOINT_URL = (
        "{origin}/xms/v1/{service_plan_id}/batches/{batch_id}/delivery_report"
    )
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self, project_id: str, request_data: GetDeliveryReportsByBatchIdRequest
    ):
        super(GetDeliveryReportByBatchIdEndpoint, self).__init__(
            project_id, request_data
        )
        self.project_id = project_id
        self.request_data = request_data

    def build_query_params(self) -> dict:
        return self.request_data.model_dump(exclude_none=True, by_alias=True)

    def handle_response(self, response: HTTPResponse) -> BatchDeliveryReport:
        try:
            super(GetDeliveryReportByBatchIdEndpoint, self).handle_response(
                response
            )
        except SmsException as e:
            raise SmsException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(response.body, BatchDeliveryReport)


class GetDeliveryReportsByPhoneNumberEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{service_plan_id}/batches/{batch_id}/delivery_report/{recipient_msisdn}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: GetDeliveryReportsByPhoneNumberRequest,
    ):
        super(GetDeliveryReportsByPhoneNumberEndpoint, self).__init__(
            project_id, request_data
        )
        self.project_id = project_id
        self.request_data = request_data

    def handle_response(
        self, response: HTTPResponse
    ) -> RecipientDeliveryReport:
        try:
            super(
                GetDeliveryReportsByPhoneNumberEndpoint, self
            ).handle_response(response)
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
    ENDPOINT_URL = "{origin}/xms/v1/{service_plan_id}/delivery_reports"
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
        return self.request_data.model_dump(exclude_none=True, by_alias=True)

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
