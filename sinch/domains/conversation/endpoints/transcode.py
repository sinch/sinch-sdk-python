from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.conversation.models.transcoding.requests import TranscodeConversationMessageRequest
from sinch.domains.conversation.models.transcoding.responses import TranscodeConversationMessageResponse


class TranscodeMessageEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/messages:transcode"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: TranscodeConversationMessageRequest):
        super(TranscodeMessageEndpoint, self).__init__(project_id, request_data)
        self.request_data = request_data
        self.project_id = project_id

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.conversation_origin,
            project_id=self.project_id
        )

    def request_body(self):
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse) -> TranscodeConversationMessageResponse:
        super(TranscodeMessageEndpoint, self).handle_response(response)
        return TranscodeConversationMessageResponse(
            transcoded_message=response.body["transcoded_message"]
        )
