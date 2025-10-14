from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.conversation.models.templates.responses import CreateConversationTemplateResponse
from sinch.domains.conversation.models.templates.requests import CreateConversationTemplateRequest


class CreateTemplateEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/templates"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: CreateConversationTemplateRequest):
        super(CreateTemplateEndpoint, self).__init__(project_id, request_data)
        self.request_data = request_data
        self.project_id = project_id

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(origin=sinch.configuration.templates_origin, project_id=self.project_id)

    def request_body(self):
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse) -> CreateConversationTemplateResponse:
        super(CreateTemplateEndpoint, self).handle_response(response)
        return CreateConversationTemplateResponse(
            id=response.body["id"],
            description=response.body["description"],
            default_translation=response.body["default_translation"],
            create_time=response.body["create_time"],
            translations=response.body["translations"],
            update_time=response.body["update_time"],
            channel=response.body["channel"],
        )
