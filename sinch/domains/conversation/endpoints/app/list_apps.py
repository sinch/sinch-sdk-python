from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.conversation.models.app.responses import ListConversationAppsResponse
from sinch.domains.conversation.models import SinchConversationApp


class ListAppsEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/apps"
    HTTP_METHOD = HTTPMethod.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str):
        super(ListAppsEndpoint, self).__init__(project_id, request_data=None)
        self.project_id = project_id

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.conversation_origin,
            project_id=self.project_id
        )

    def handle_response(self, response: HTTPResponse) -> ListConversationAppsResponse:
        super(ListAppsEndpoint, self).handle_response(response)
        return ListConversationAppsResponse(
            apps=[
                SinchConversationApp(
                    id=contact["id"],
                    channel_credentials=contact["channel_credentials"],
                    processing_mode=contact["processing_mode"],
                    conversation_metadata_report_view=contact["conversation_metadata_report_view"],
                    display_name=contact["display_name"],
                    rate_limits=contact["rate_limits"],
                    retention_policy=contact["retention_policy"],
                    dispatch_retention_policy=contact["dispatch_retention_policy"],
                    smart_conversation=contact["smart_conversation"]
                ) for contact in response.body["apps"]
            ]
        )
