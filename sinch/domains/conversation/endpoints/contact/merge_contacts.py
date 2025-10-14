import json
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.conversation.models.contact.responses import MergeConversationContactsResponse


class MergeConversationContactsEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/contacts/{destination_id}:merge"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id, request_data):
        super(MergeConversationContactsEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.conversation_origin,
            project_id=self.project_id,
            destination_id=self.request_data.destination_id,
        )

    def request_body(self):
        return json.dumps({"source_id": self.request_data.source_id})

    def handle_response(self, response: HTTPResponse) -> MergeConversationContactsResponse:
        super(MergeConversationContactsEndpoint, self).handle_response(response)
        return MergeConversationContactsResponse(**response.body)
