from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.conversation.models.contact.responses import CreateConversationContactResponse
from sinch.domains.conversation.models.contact.requests import CreateConversationContactRequest


class CreateConversationContactEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/contacts"
    HTTP_METHOD = HTTPMethod.POST
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH

    def __init__(self, project_id: str, request_data: CreateConversationContactRequest):
        super(CreateConversationContactEndpoint, self).__init__(project_id, request_data)
        self.request_data = request_data
        self.project_id = project_id

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.conversation_origin,
            project_id=self.project_id
        )

    def request_body(self):
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse) -> CreateConversationContactResponse:
        super(CreateConversationContactEndpoint, self).handle_response(response)
        return CreateConversationContactResponse(
            id=response.body["id"],
            channel_identities=response.body["channel_identities"],
            channel_priority=response.body["channel_priority"],
            display_name=response.body["display_name"],
            email=response.body["email"],
            external_id=response.body["external_id"],
            metadata=response.body["metadata"],
            language=response.body["language"]
        )
