from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.conversation.models.message.responses import DeleteConversationMessageResponse
from sinch.domains.conversation.models.message.requests import DeleteConversationMessageRequest


class DeleteConversationMessageEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/messages/{message_id}"
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: DeleteConversationMessageRequest):
        super(DeleteConversationMessageEndpoint, self).__init__(project_id, request_data)
        self.request_data = request_data
        self.project_id = project_id

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.conversation_origin,
            project_id=self.project_id,
            message_id=self.request_data.message_id
        )

    def build_query_params(self):
        if self.request_data.messages_source:
            return {
                "messages_source": self.request_data.messages_source
            }

    def handle_response(self, response: HTTPResponse) -> DeleteConversationMessageResponse:
        return DeleteConversationMessageResponse()
