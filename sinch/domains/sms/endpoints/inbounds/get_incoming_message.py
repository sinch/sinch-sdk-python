from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.endpoints.sms_endpoint import SMSEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.sms.models.inbounds.requests import GetSMSInboundMessageRequest
from sinch.domains.sms.models.inbounds.responses import GetInboundMessagesResponse


class GetInboundMessagesEndpoint(SMSEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/inbounds/{inbound_id}"
    HTTP_METHOD = HTTPMethod.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: GetSMSInboundMessageRequest):
        super(GetInboundMessagesEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.sms_origin,
            project_id=self.project_id,
            inbound_id=self.request_data.inbound_id
        )

    def handle_response(self, response: HTTPResponse):
        super(GetInboundMessagesEndpoint, self).handle_response(response)
        return GetInboundMessagesResponse(
            type=response.body.get("type"),
            id=response.body.get("id"),
            origin_number=response.body.get("from"),
            destination_number=response.body.get("to"),
            body=response.body.get("body"),
            operator_id=response.body.get("operator_id"),
            send_at=response.body.get("send_at"),
            received_at=response.body.get("received_at")
        )
