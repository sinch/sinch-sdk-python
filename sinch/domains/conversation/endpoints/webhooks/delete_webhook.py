from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.conversation.models.webhook.responses import SinchDeleteWebhookResponse
from sinch.domains.conversation.models.webhook.requests import DeleteConversationWebhookRequest


class DeleteWebhookEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/webhooks/{webhook_id}"
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: DeleteConversationWebhookRequest):
        super(DeleteWebhookEndpoint, self).__init__(project_id, request_data)
        self.request_data = request_data
        self.project_id = project_id

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.conversation_origin,
            project_id=self.project_id,
            webhook_id=self.request_data.webhook_id,
        )

    def handle_response(self, response: HTTPResponse) -> SinchDeleteWebhookResponse:
        super(DeleteWebhookEndpoint, self).handle_response(response)
        return SinchDeleteWebhookResponse()
