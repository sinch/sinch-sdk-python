from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.conversation.models.opt_in_opt_out.requests import RegisterConversationOptInRequest
from sinch.domains.conversation.models.opt_in_opt_out.responses import RegisterConversationOptInResponse


class RegisterOptInEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/optins:register"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: RegisterConversationOptInRequest):
        super(RegisterOptInEndpoint, self).__init__(project_id, request_data)
        self.request_data = request_data
        self.project_id = project_id

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(origin=sinch.configuration.conversation_origin, project_id=self.project_id)

    def build_query_params(self):
        if self.request_data.request_id:
            return {"request_id": self.request_data.request_id}

    def request_body(self):
        self.request_data.request_id = None
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse) -> RegisterConversationOptInResponse:
        super(RegisterOptInEndpoint, self).handle_response(response)
        return RegisterConversationOptInResponse(response.body["request_id"], response.body["opt_in"])
