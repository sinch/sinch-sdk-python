from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.conversation.models.contact.requests import GetConversationContactRequest
from sinch.domains.conversation.models.contact.responses import GetConversationContactResponse


class GetContactEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/contacts/{contact_id}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id, request_data: GetConversationContactRequest):
        super(GetContactEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.conversation_origin,
            project_id=self.project_id,
            contact_id=self.request_data.contact_id
        )

    def handle_response(self, response: HTTPResponse) -> GetConversationContactResponse:
        super(GetContactEndpoint, self).handle_response(response)
        return GetConversationContactResponse(
            id=response.body["id"],
            channel_identities=response.body["channel_identities"],
            channel_priority=response.body["channel_priority"],
            display_name=response.body["display_name"],
            email=response.body["email"],
            external_id=response.body["external_id"],
            metadata=response.body["metadata"],
            language=response.body["language"]
        )
