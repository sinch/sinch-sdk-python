from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.conversation.models.capability.requests import QueryConversationCapabilityRequest
from sinch.domains.conversation.models.capability.responses import QueryConversationCapabilityResponse


class CapabilityQueryEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/capability:query"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: QueryConversationCapabilityRequest):
        super(CapabilityQueryEndpoint, self).__init__(project_id, request_data)
        self.request_data = request_data
        self.project_id = project_id

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.conversation_origin,
            project_id=self.project_id
        )

    def request_body(self):
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse) -> QueryConversationCapabilityResponse:
        super(CapabilityQueryEndpoint, self).handle_response(response)
        return QueryConversationCapabilityResponse(
            request_id=response.body["request_id"],
            app_id=response.body["app_id"],
            recipient=response.body["recipient"],
        )
