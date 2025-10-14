from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.conversation.models.webhook.responses import SinchListWebhooksResponse
from sinch.domains.conversation.models.webhook.requests import ListConversationWebhookRequest
from sinch.domains.conversation.models.webhook import ConversationWebhook


class ListWebhooksEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/apps/{app_id}/webhooks"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: ListConversationWebhookRequest):
        super(ListWebhooksEndpoint, self).__init__(project_id, request_data)
        self.request_data = request_data
        self.project_id = project_id

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.conversation_origin, project_id=self.project_id, app_id=self.request_data.app_id
        )

    def handle_response(self, response: HTTPResponse) -> SinchListWebhooksResponse:
        super(ListWebhooksEndpoint, self).handle_response(response)
        return SinchListWebhooksResponse(
            webhooks=[
                ConversationWebhook(
                    id=webhook["id"],
                    app_id=webhook["app_id"],
                    target=webhook["target"],
                    target_type=webhook["target_type"],
                    secret=webhook["secret"],
                    triggers=webhook["triggers"],
                    client_credentials=webhook["client_credentials"],
                )
                for webhook in response.body["webhooks"]
            ]
        )
