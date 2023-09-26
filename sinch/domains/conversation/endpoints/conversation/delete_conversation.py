from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.conversation.models.conversation.responses import SinchDeleteConversationResponse
from sinch.domains.conversation.models.conversation.requests import DeleteConversationRequest


class DeleteConversationEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/conversations/{conversation_id}"
    HTTP_METHOD = HTTPMethod.DELETE
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH

    def __init__(self, project_id: str, request_data: DeleteConversationRequest):
        super(DeleteConversationEndpoint, self).__init__(project_id, request_data)
        self.request_data = request_data
        self.project_id = project_id

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.conversation_origin,
            project_id=self.project_id,
            conversation_id=self.request_data.conversation_id
        )

    def handle_response(self, response: HTTPResponse) -> SinchDeleteConversationResponse:
        super(DeleteConversationEndpoint, self).handle_response(response)
        return SinchDeleteConversationResponse()
