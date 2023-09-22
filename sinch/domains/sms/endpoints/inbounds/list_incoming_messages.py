from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.endpoints.sms_endpoint import SMSEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.sms.models.inbounds import InboundMessage
from sinch.domains.sms.models.inbounds.requests import ListSMSInboundMessageRequest
from sinch.domains.sms.models.inbounds.responses import SinchListInboundMessagesResponse


class ListInboundMessagesEndpoint(SMSEndpoint):
    ENDPOINT_URL = "{origin}/xms/v1/{project_id}/inbounds"
    HTTP_METHOD = HTTPMethod.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: ListSMSInboundMessageRequest):
        super(ListInboundMessagesEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.sms_origin,
            project_id=self.project_id
        )

    def build_query_params(self):
        return self.request_data.as_dict()

    def handle_response(self, response: HTTPResponse):
        super(ListInboundMessagesEndpoint, self).handle_response(response)
        return SinchListInboundMessagesResponse(
            inbounds=[
                InboundMessage(
                    type=inbound.get("type"),
                    id=inbound.get("id"),
                    from_=inbound.get("from"),
                    to=inbound.get("to"),
                    body=inbound.get("body"),
                    operator_id=inbound.get("operator_id"),
                    send_at=inbound.get("send_at"),
                    received_at=inbound.get("received_at"),
                    client_reference=inbound.get("client_reference")
                ) for inbound in response.body["inbounds"]
            ],
            page=response.body.get("page"),
            page_size=response.body.get("page_size"),
            count=response.body.get("count")
        )
