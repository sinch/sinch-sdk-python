from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.conversation.models.webhook.responses import CreateWebhookResponse
from sinch.domains.conversation.models.webhook.requests import CreateConversationWebhookRequest


class CreateWebhookEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/webhooks"
    HTTP_METHOD = HTTPMethod.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: CreateConversationWebhookRequest):
        super(CreateWebhookEndpoint, self).__init__(project_id, request_data)
        self.request_data = request_data
        self.project_id = project_id

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.conversation_origin,
            project_id=self.project_id
        )

    def request_body(self):
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse) -> CreateWebhookResponse:
        super(CreateWebhookEndpoint, self).handle_response(response)
        return CreateWebhookResponse(
            id=response.body["id"],
            app_id=response.body["app_id"],
            target=response.body["target"],
            target_type=response.body["target_type"],
            secret=response.body["secret"],
            triggers=response.body["triggers"],
            client_credentials=response.body["client_credentials"]
        )
