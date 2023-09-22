from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.conversation.models.app.responses import DeleteConversationAppResponse
from sinch.domains.conversation.models.app.requests import DeleteConversationAppRequest


class DeleteConversationAppEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/apps/{app_id}"
    HTTP_METHOD = HTTPMethod.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: DeleteConversationAppRequest):
        super(DeleteConversationAppEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.conversation_origin,
            project_id=self.project_id,
            app_id=self.request_data.app_id
        )

    def handle_response(self, response: HTTPResponse) -> DeleteConversationAppResponse:
        super(DeleteConversationAppEndpoint, self).handle_response(response)
        return DeleteConversationAppResponse()
