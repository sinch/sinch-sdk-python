from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.conversation.models.app.responses import UpdateConversationAppResponse
from sinch.domains.conversation.models.app.requests import UpdateConversationAppRequest


class UpdateConversationAppEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/apps/{app_id}"
    HTTP_METHOD = HTTPMethod.PATCH
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH

    def __init__(self, project_id: str, request_data: UpdateConversationAppRequest):
        super(UpdateConversationAppEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.conversation_origin,
            project_id=self.project_id,
            app_id=self.request_data.app_id
        )

    def build_query_params(self):
        if self.request_data.update_mask:
            return {"update_mask.paths": self.request_data.update_mask}

    def request_body(self):
        self.request_data.update_mask = None
        self.request_data.app_id = None
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse) -> UpdateConversationAppResponse:
        super(UpdateConversationAppEndpoint, self).handle_response(response)
        return UpdateConversationAppResponse(
            id=response.body["id"],
            channel_credentials=response.body["channel_credentials"],
            processing_mode=response.body["processing_mode"],
            conversation_metadata_report_view=response.body["conversation_metadata_report_view"],
            display_name=response.body["display_name"],
            rate_limits=response.body["rate_limits"],
            retention_policy=response.body["retention_policy"],
            dispatch_retention_policy=response.body["dispatch_retention_policy"],
            smart_conversation=response.body["smart_conversation"]
        )
