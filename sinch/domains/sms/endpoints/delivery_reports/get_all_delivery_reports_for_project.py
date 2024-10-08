from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.endpoints.sms_endpoint import SMSEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.sms.models.delivery_reports import DeliveryReport
from sinch.domains.sms.models.delivery_reports.requests import ListSMSDeliveryReportsRequest
from sinch.domains.sms.models.delivery_reports.responses import ListSMSDeliveryReportsResponse


class ListDeliveryReportsEndpoint(SMSEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_or_service_id}/delivery_reports"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, request_data: ListSMSDeliveryReportsRequest, sinch):
        super().__init__(request_data, sinch)

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.sms_origin,
            project_or_service_id=self.project_or_service_id
        )

    def build_query_params(self):
        return self.request_data.as_dict()

    def handle_response(self, response: HTTPResponse):
        super(ListDeliveryReportsEndpoint, self).handle_response(response)
        return ListSMSDeliveryReportsResponse(
            delivery_reports=[
                DeliveryReport(
                    at=delivery_report.get("at"),
                    batch_id=delivery_report.get("batch_id"),
                    code=delivery_report.get("code"),
                    recipient=delivery_report.get("recipient"),
                    status=delivery_report.get("status"),
                    applied_originator=delivery_report.get("applied_originator"),
                    client_reference=delivery_report.get("client_reference"),
                    encoding=delivery_report.get("encoding"),
                    number_of_message_parts=delivery_report.get("number_of_message_parts"),
                    operator=delivery_report.get("operator"),
                    operator_status_at=delivery_report.get("operator_status_at"),
                    type=delivery_report.get("type")
                ) for delivery_report in response.body["delivery_reports"]
            ],
            page=response.body.get("page"),
            page_size=response.body.get("page_size"),
            count=response.body.get("count")
        )
