from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.conversation.models.event.requests import SendConversationEventRequest
from sinch.domains.conversation.models.event.responses import SendConversationEventResponse


class SendEventEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/events:send"
    HTTP_METHOD = HTTPMethod.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: SendConversationEventRequest):
        super(SendEventEndpoint, self).__init__(project_id, request_data)
        self.request_data = request_data
        self.project_id = project_id

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.conversation_origin,
            project_id=self.project_id
        )

    def request_body(self):
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse) -> SendConversationEventResponse:
        super(SendEventEndpoint, self).handle_response(response)
        return SendConversationEventResponse(
            accepted_time=response.body["accepted_time"],
            event_id=response.body["event_id"]
        )
