from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.conversation.models.contact.requests import GetConversationChannelProfileRequest
from sinch.domains.conversation.models.contact.responses import GetConversationChannelProfileResponse


class GetChannelProfileEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/contacts:getChannelProfile"
    HTTP_METHOD = HTTPMethod.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: GetConversationChannelProfileRequest):
        super(GetChannelProfileEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.conversation_origin,
            project_id=self.project_id
        )

    def request_body(self):
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse) -> GetConversationChannelProfileResponse:
        super(GetChannelProfileEndpoint, self).handle_response(response)
        return GetConversationChannelProfileResponse(
            profile_name=response.body.get("profile_name")
        )
