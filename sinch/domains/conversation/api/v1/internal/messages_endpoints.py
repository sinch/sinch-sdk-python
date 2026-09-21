from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.conversation.api.v1.internal.base import (
    ConversationEndpoint,
)
from sinch.domains.conversation.models.v1.messages.internal import (
    ListMessagesResponse,
)
from sinch.domains.conversation.models.v1.messages.internal.request import (
    ListLastMessagesByChannelIdentityRequest,
    ListMessagesRequest,
    MessageIdRequest,
    SendMessageRequest,
    UpdateMessageMetadataRequest,
)
from sinch.domains.conversation.models.v1.messages.response import (
    SendMessageResponse,
)
from sinch.domains.conversation.models.v1.messages.response.types import (
    ConversationMessageResponse,
)


class MessageEndpoint(ConversationEndpoint):
    """
    Base class for message-related endpoints that share common query parameter handling.
    """

    UNSET_SERIALIZATION: bool = False
    QUERY_PARAM_FIELDS = {"messages_source"}
    #: request_data fields sent in the body, as an allowlist,
    #: PATCH endpoints only send an explicit subset of fields).
    BODY_PARAM_FIELDS = set()


class ListMessagesEndpoint(MessageEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/messages"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS = {
        "app_id",
        "channel",
        "channel_identity",
        "contact_id",
        "conversation_id",
        "direction",
        "end_time",
        "messages_source",
        "only_recipient_originated",
        "page_size",
        "page_token",
        "start_time",
        "view",
    }

    def __init__(
        self,
        project_id: str,
        request_data: ListMessagesRequest,
        response_model=ListMessagesResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class ListLastMessagesByChannelIdentityEndpoint(ConversationEndpoint):
    ENDPOINT_URL = (
        "{origin}/v1/projects/{project_id}/messages:fetch-last-message"
    )
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: ListLastMessagesByChannelIdentityRequest,
        response_model=ListMessagesResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class DeleteMessageEndpoint(MessageEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/messages/{message_id}"
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: MessageIdRequest):
        super().__init__(project_id, request_data)


class GetMessageEndpoint(MessageEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/messages/{message_id}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: MessageIdRequest,
        response_model=ConversationMessageResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class UpdateMessageMetadataEndpoint(MessageEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/messages/{message_id}"
    HTTP_METHOD = HTTPMethods.PATCH.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    BODY_PARAM_FIELDS = {"metadata"}

    def __init__(
        self,
        project_id: str,
        request_data: UpdateMessageMetadataRequest,
        response_model=ConversationMessageResponse,
    ):
        super().__init__(project_id, request_data, response_model)

    def request_body(self) -> str:
        """Only BODY_PARAM_FIELDS are sent, not request_data minus path/query params."""
        body = self.request_data.model_dump_json(
            by_alias=True, exclude_none=True, include=self.BODY_PARAM_FIELDS
        )
        return body if body != "{}" else ""


class SendMessageEndpoint(ConversationEndpoint):
    UNSET_SERIALIZATION: bool = False
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/messages:send"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: SendMessageRequest,
        response_model=SendMessageResponse,
    ):
        super().__init__(project_id, request_data, response_model)
