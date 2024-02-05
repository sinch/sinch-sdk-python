from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.endpoints.sms_endpoint import SMSEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.sms.models.batches.responses import SendSMSBatchResponse
from sinch.domains.sms.models.batches.requests import SendBatchRequest


class SendBatchSMSEndpoint(SMSEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/batches"
    HTTP_METHOD = HTTPMethod.POST
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH

    def __init__(self, project_id: str, request_data: SendBatchRequest):
        super(SendBatchSMSEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.sms_origin,
            project_id=self.project_id
        )

    def request_body(self):
        self.request_data.batch_id = None
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse):
        super(SendBatchSMSEndpoint, self).handle_response(response)
        return SendSMSBatchResponse(
            id=response.body.get("id"),
            to=response.body.get("to"),
            from_=response.body.get("from"),
            body=response.body.get("body"),
            delivery_report=response.body.get("delivery_report"),
            cancelled=response.body.get("cancelled"),
            type=response.body.get("type"),
            campaign_id=response.body.get("campaign_id"),
            created_at=response.body.get("created_at"),
            modified_at=response.body.get("modified_at"),
            send_at=response.body.get("send_at"),
            expire_at=response.body.get("expire_at")
        )
