from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.conversation.models.app.responses import CreateConversationAppResponse
from sinch.domains.conversation.models.app.requests import CreateConversationAppRequest


class CreateConversationAppEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/apps"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: CreateConversationAppRequest):
        super(CreateConversationAppEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(origin=sinch.configuration.conversation_origin, project_id=self.project_id)

    def request_body(self):
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse) -> CreateConversationAppResponse:
        super(CreateConversationAppEndpoint, self).handle_response(response)
        return CreateConversationAppResponse(
            id=response.body["id"],
            channel_credentials=response.body["channel_credentials"],
            processing_mode=response.body["processing_mode"],
            conversation_metadata_report_view=response.body["conversation_metadata_report_view"],
            display_name=response.body["display_name"],
            rate_limits=response.body["rate_limits"],
            retention_policy=response.body["retention_policy"],
            dispatch_retention_policy=response.body["dispatch_retention_policy"],
            smart_conversation=response.body["smart_conversation"],
        )
