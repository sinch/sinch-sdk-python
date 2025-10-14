from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.conversation.models.conversation.responses import SinchStopConversationResponse
from sinch.domains.conversation.models.conversation.requests import StopConversationRequest


class StopConversationEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/conversations/{conversation_id}:stop"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: StopConversationRequest):
        super(StopConversationEndpoint, self).__init__(project_id, request_data)
        self.request_data = request_data
        self.project_id = project_id

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.conversation_origin,
            project_id=self.project_id,
            conversation_id=self.request_data.conversation_id,
        )

    def handle_response(self, response: HTTPResponse) -> SinchStopConversationResponse:
        super(StopConversationEndpoint, self).handle_response(response)
        return SinchStopConversationResponse()
