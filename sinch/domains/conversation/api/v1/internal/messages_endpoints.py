import json
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.models.v1.messages.internal.request import (
    ListMessagesRequest,
    ListLastMessagesByChannelIdentityRequest,
    MessageIdRequest,
    UpdateMessageMetadataRequest,
    SendMessageRequest,
)
from sinch.domains.conversation.models.v1.messages.internal import (
    ListMessagesResponse,
)
from sinch.domains.conversation.models.v1.messages.response.types import (
    ConversationMessageResponse,
)
from sinch.domains.conversation.models.v1.messages.response import (
    SendMessageResponse,
)
from sinch.domains.conversation.api.v1.internal.base import (
    ConversationEndpoint,
)
from sinch.domains.conversation.api.v1.exceptions import ConversationException


class ListMessagesResponseMixin:
    """
    Mixin for endpoints that return ListMessagesResponse; centralizes response handling.
    """

    def handle_response(self, response: HTTPResponse) -> ListMessagesResponse:
        try:
            super().handle_response(response)
        except ConversationException as e:
            raise ConversationException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(response.body, ListMessagesResponse)


class MessageEndpoint(ConversationEndpoint):
    """
    Base class for message-related endpoints that share common query parameter handling.
    """

    QUERY_PARAM_FIELDS = {"messages_source"}
    BODY_PARAM_FIELDS = set()

    def build_query_params(self) -> dict:
        path_params = self._get_path_params_from_url()
        exclude_set = path_params.union(self.BODY_PARAM_FIELDS)
        query_params = self.request_data.model_dump(
            include=self.QUERY_PARAM_FIELDS,
            exclude_none=True,
            by_alias=True,
            exclude=exclude_set,
        )
        return query_params


class ListMessagesEndpoint(ListMessagesResponseMixin, MessageEndpoint):
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

    def __init__(self, project_id: str, request_data: ListMessagesRequest):
        super(ListMessagesEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data


class ListLastMessagesByChannelIdentityEndpoint(
    ListMessagesResponseMixin, ConversationEndpoint
):
    ENDPOINT_URL = (
        "{origin}/v1/projects/{project_id}/messages:fetch-last-message"
    )
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: ListLastMessagesByChannelIdentityRequest,
    ):
        super(ListLastMessagesByChannelIdentityEndpoint, self).__init__(
            project_id, request_data
        )
        self.project_id = project_id
        self.request_data = request_data

    def request_body(self):
        request_data_dict = self.request_data.model_dump(
            mode="json", by_alias=True, exclude_none=True
        )
        return json.dumps(request_data_dict)


class DeleteMessageEndpoint(MessageEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/messages/{message_id}"
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: MessageIdRequest):
        super(DeleteMessageEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def handle_response(self, response: HTTPResponse):
        try:
            super(DeleteMessageEndpoint, self).handle_response(response)
        except ConversationException as e:
            raise ConversationException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )


class GetMessageEndpoint(MessageEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/messages/{message_id}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: MessageIdRequest):
        super(GetMessageEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def handle_response(
        self, response: HTTPResponse
    ) -> ConversationMessageResponse:
        try:
            super(GetMessageEndpoint, self).handle_response(response)
        except ConversationException as e:
            raise ConversationException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(
            response.body, ConversationMessageResponse
        )


class UpdateMessageMetadataEndpoint(MessageEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/messages/{message_id}"
    HTTP_METHOD = HTTPMethods.PATCH.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    BODY_PARAM_FIELDS = {"metadata"}

    def __init__(
        self, project_id: str, request_data: UpdateMessageMetadataRequest
    ):
        super(UpdateMessageMetadataEndpoint, self).__init__(
            project_id, request_data
        )
        self.project_id = project_id
        self.request_data = request_data

    def request_body(self):
        path_params = self._get_path_params_from_url()
        exclude_set = path_params.union(self.QUERY_PARAM_FIELDS)
        request_data = self.request_data.model_dump(
            include=self.BODY_PARAM_FIELDS,
            by_alias=True,
            exclude_none=True,
            exclude=exclude_set,
        )
        return json.dumps(request_data)

    def handle_response(
        self, response: HTTPResponse
    ) -> ConversationMessageResponse:
        try:
            super(UpdateMessageMetadataEndpoint, self).handle_response(
                response
            )
        except ConversationException as e:
            raise ConversationException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(
            response.body, ConversationMessageResponse
        )


class SendMessageEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/messages:send"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: SendMessageRequest):
        super(SendMessageEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def request_body(self):
        request_data_dict = self.request_data.model_dump(
            mode="json",
            by_alias=True,
            exclude_none=True,
        )
        return json.dumps(request_data_dict)

    def handle_response(self, response: HTTPResponse) -> SendMessageResponse:
        try:
            super(SendMessageEndpoint, self).handle_response(response)
        except ConversationException as e:
            raise ConversationException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(response.body, SendMessageResponse)
