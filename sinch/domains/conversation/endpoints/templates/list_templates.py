from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.conversation.models.templates.responses import ListConversationTemplatesResponse
from sinch.domains.conversation.models.templates import ConversationTemplate


class ListTemplatesEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/templates"
    HTTP_METHOD = HTTPMethod.GET
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH

    def __init__(self, project_id: str, request_data=None):
        super(ListTemplatesEndpoint, self).__init__(project_id, request_data)
        self.request_data = request_data
        self.project_id = project_id

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.templates_origin,
            project_id=self.project_id
        )

    def handle_response(self, response: HTTPResponse) -> ListConversationTemplatesResponse:
        super(ListTemplatesEndpoint, self).handle_response(response)
        return ListConversationTemplatesResponse(
            templates=[
                ConversationTemplate(
                    id=template["id"],
                    description=template["description"],
                    default_translation=template["default_translation"],
                    create_time=template["create_time"],
                    translations=template["translations"],
                    update_time=template["update_time"],
                    channel=template["channel"]
                ) for template in response.body["templates"]
            ]
        )
