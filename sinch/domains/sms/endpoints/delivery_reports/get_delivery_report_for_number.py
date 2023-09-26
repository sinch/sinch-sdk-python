from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.endpoints.sms_endpoint import SMSEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.sms.models.delivery_reports.requests import GetSMSDeliveryReportForNumberRequest
from sinch.domains.sms.models.delivery_reports.responses import GetSMSDeliveryReportForNumberResponse


class GetDeliveryReportForNumberEndpoint(SMSEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/batches/{batch_id}/delivery_report/{recipient_msisdn}"
    HTTP_METHOD = HTTPMethod.GET
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH

    def __init__(self, project_id: str, request_data: GetSMSDeliveryReportForNumberRequest):
        super(GetDeliveryReportForNumberEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.sms_origin,
            project_id=self.project_id,
            batch_id=self.request_data.batch_id,
            recipient_msisdn=self.request_data.recipient_number
        )

    def handle_response(self, response: HTTPResponse):
        super(GetDeliveryReportForNumberEndpoint, self).handle_response(response)
        return GetSMSDeliveryReportForNumberResponse(
            at=response.body.get("at"),
            batch_id=response.body.get("batch_id"),
            code=response.body.get("code"),
            recipient=response.body.get("recipient"),
            status=response.body.get("status"),
            applied_originator=response.body.get("applied_originator"),
            client_reference=response.body.get("client_reference"),
            number_of_message_parts=response.body.get("number_of_message_parts"),
            operator=response.body.get("operator"),
            operator_status_at=response.body.get("operator_status_at"),
            type=response.body.get("type")
        )
