from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.conversation.models.templates.responses import DeleteConversationTemplateResponse
from sinch.domains.conversation.models.templates.requests import DeleteConversationTemplateRequest


class DeleteTemplateEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/templates/{template_id}"
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: DeleteConversationTemplateRequest):
        super(DeleteTemplateEndpoint, self).__init__(project_id, request_data)
        self.request_data = request_data
        self.project_id = project_id

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.templates_origin,
            project_id=self.project_id,
            template_id=self.request_data.template_id,
        )

    def handle_response(self, response: HTTPResponse) -> DeleteConversationTemplateResponse:
        super(DeleteTemplateEndpoint, self).handle_response(response)
        return DeleteConversationTemplateResponse()
