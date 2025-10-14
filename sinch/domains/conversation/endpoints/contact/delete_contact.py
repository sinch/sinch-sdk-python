from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.conversation.models.contact.responses import DeleteConversationContactResponse


class DeleteContactEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/contacts/{contact_id}"
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id, request_data):
        super(DeleteContactEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.conversation_origin,
            project_id=self.project_id,
            contact_id=self.request_data.contact_id,
        )

    def handle_response(self, response: HTTPResponse) -> DeleteConversationContactResponse:
        super(DeleteContactEndpoint, self).handle_response(response)
        return DeleteConversationContactResponse()
