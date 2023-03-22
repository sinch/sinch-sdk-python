from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.endpoints.sms_endpoint import SMSEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.sms.models.batches.responses import SendSMSDeliveryFeedbackResponse
from sinch.domains.sms.models.batches.requests import SendDeliveryFeedbackRequest


class SendDeliveryReportEndpoint(SMSEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/batches/{batch_id}/delivery_feedback"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: SendDeliveryFeedbackRequest):
        super(SendDeliveryReportEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.sms_origin,
            project_id=self.project_id,
            batch_id=self.request_data.batch_id
        )

    def request_body(self):
        self.request_data.batch_id = None
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse):
        super(SendDeliveryReportEndpoint, self).handle_response(response)
        return SendSMSDeliveryFeedbackResponse()
