from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.conversation.models.conversation.responses import SinchUpdateConversationResponse
from sinch.domains.conversation.models.conversation.requests import UpdateConversationRequest


class UpdateConversationEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/conversations/{conversation_id}"
    HTTP_METHOD = HTTPMethods.PATCH.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: UpdateConversationRequest):
        super(UpdateConversationEndpoint, self).__init__(project_id, request_data)
        self.request_data = request_data
        self.project_id = project_id

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.conversation_origin,
            project_id=self.project_id,
            conversation_id=self.request_data.conversation_id
        )

    def request_body(self):
        self.request_data.conversation_id = None
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse) -> SinchUpdateConversationResponse:
        super(UpdateConversationEndpoint, self).handle_response(response)
        return SinchUpdateConversationResponse(
            id=response.body["id"],
            app_id=response.body["app_id"],
            contact_id=response.body["contact_id"],
            last_received=response.body["last_received"],
            active_channel=response.body["active_channel"],
            active=response.body["active"],
            metadata=response.body["metadata"],
            metadata_json=response.body["metadata_json"]
        )
