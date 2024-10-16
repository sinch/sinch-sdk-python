from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.endpoints.sms_endpoint import SMSEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.sms.models.delivery_reports.requests import GetSMSDeliveryReportForBatchRequest
from sinch.domains.sms.models.delivery_reports.responses import GetSMSDeliveryReportForBatchResponse


class GetDeliveryReportForBatchEndpoint(SMSEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_or_service_id}/batches/{batch_id}/delivery_report"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, request_data: GetSMSDeliveryReportForBatchRequest, sinch):
        super().__init__(request_data, sinch)

    def build_query_params(self):
        params = {}
        if self.request_data.type_:
            params["type"] = self.request_data.type_

        if self.request_data.status:
            params["status"] = self.request_data.status

        if self.request_data.code:
            params["code"] = list(map(str, self.request_data.code))

        return params

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.sms_origin,
            project_or_service_id=self.project_or_service_id,
            batch_id=self.request_data.batch_id
        )

    def handle_response(self, response: HTTPResponse):
        super(GetDeliveryReportForBatchEndpoint, self).handle_response(response)
        return GetSMSDeliveryReportForBatchResponse(
            type=response.body.get("type"),
            batch_id=response.body.get("batch_id"),
            total_message_count=response.body.get("total_message_count"),
            statuses=response.body.get("statuses"),
            client_reference=response.body.get("client_reference")
        )
