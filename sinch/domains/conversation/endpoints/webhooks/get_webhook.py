from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.conversation.models.webhook.responses import GetWebhookResponse
from sinch.domains.conversation.models.webhook.requests import GetConversationWebhookRequest


class GetWebhookEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/webhooks/{webhook_id}"
    HTTP_METHOD = HTTPMethod.GET
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH

    def __init__(self, project_id: str, request_data: GetConversationWebhookRequest):
        super(GetWebhookEndpoint, self).__init__(project_id, request_data)
        self.request_data = request_data
        self.project_id = project_id

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.conversation_origin,
            project_id=self.project_id,
            webhook_id=self.request_data.webhook_id
        )

    def handle_response(self, response: HTTPResponse) -> GetWebhookResponse:
        super(GetWebhookEndpoint, self).handle_response(response)
        return GetWebhookResponse(
            id=response.body["id"],
            app_id=response.body["app_id"],
            target=response.body["target"],
            target_type=response.body["target_type"],
            secret=response.body["secret"],
            triggers=response.body["triggers"],
            client_credentials=response.body["client_credentials"]
        )
