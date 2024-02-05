from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.conversation.models.contact.responses import ListConversationContactsResponse
from sinch.domains.conversation.models import SinchConversationContact


class ListContactsEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/contacts"
    HTTP_METHOD = HTTPMethod.GET
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH

    def __init__(self, project_id, request_data):
        super(ListContactsEndpoint, self).__init__(project_id, request_data)
        self.request_data = request_data
        self.project_id = project_id

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.conversation_origin,
            project_id=self.project_id
        )

    def build_query_params(self):
        params = {}
        if self.request_data.page_size:
            params["page_size"] = self.request_data.page_size

        if self.request_data.page_token:
            params["page_token"] = self.request_data.page_token

        return params

    def handle_response(self, response: HTTPResponse) -> ListConversationContactsResponse:
        super(ListContactsEndpoint, self).handle_response(response)
        return ListConversationContactsResponse(
            contacts=[SinchConversationContact(
                id=contact["id"],
                channel_identities=contact["channel_identities"],
                channel_priority=contact["channel_priority"],
                display_name=contact["display_name"],
                email=contact["email"],
                external_id=contact["external_id"],
                metadata=contact["metadata"],
                language=contact["language"]
            ) for contact in response.body["contacts"]],
            next_page_token=response.body.get("next_page_token")
        )
