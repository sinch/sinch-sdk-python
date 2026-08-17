from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.sms.api.v1.internal.base import SmsEndpoint
from sinch.domains.sms.models.v1.internal import (
    GetBatchDeliveryReportRequest,
    GetRecipientDeliveryReportRequest,
    ListDeliveryReportsRequest,
    ListDeliveryReportsResponse,
)
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

    QUERY_PARAM_FIELDS: set = {
        "batch_id",
        "type",
        "client_reference",
    }
    QUERY_PARAM_FIELDS_EXPLODE_FALSE: set = {"status", "code"}

    def __init__(
        self,
        project_id: str,
        request_data: GetBatchDeliveryReportRequest,
        response_model=BatchDeliveryReport,
    ):
        super().__init__(project_id, request_data, response_model)


class GetRecipientDeliveryReportEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/batches/{batch_id}/delivery_report/{recipient_msisdn}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: GetRecipientDeliveryReportRequest,
        response_model=RecipientDeliveryReport,
    ):
        super().__init__(project_id, request_data, response_model)


class ListDeliveryReportsEndpoint(SmsEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/delivery_reports"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS: set = {
        "page",
        "page_size",
        "start_date",
        "end_date",
        "client_reference",
    }
    QUERY_PARAM_FIELDS_EXPLODE_FALSE: set = {"status", "code"}

    def __init__(
        self,
        project_id: str,
        request_data: ListDeliveryReportsRequest,
        response_model=ListDeliveryReportsResponse,
    ):
        super().__init__(project_id, request_data, response_model)
