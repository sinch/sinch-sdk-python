from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.conversation.api.v1.internal.base.conversation_endpoint import (
    ConversationEndpoint,
)
from sinch.domains.conversation.models.v1.transcoding.internal.transcode_message_request import (
    TranscodeMessageRequest,
)
from sinch.domains.conversation.models.v1.transcoding.response.transcode_message_response import (
    TranscodeMessageResponse,
)


class TranscodeMessageEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/messages:transcode"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: TranscodeMessageRequest,
        response_model=TranscodeMessageResponse,
    ):
        super().__init__(project_id, request_data, response_model)
