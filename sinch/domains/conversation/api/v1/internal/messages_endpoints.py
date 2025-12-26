import json
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.models.v1.messages.internal import (
    DeleteMessageRequest,
    GetMessageRequest,
    UpdateMessageMetadataRequest,
)
from sinch.domains.conversation.models.v1.messages.types import (
    ConversationMessageResponse,
)
from sinch.domains.conversation.api.v1.internal.base import (
    ConversationEndpoint,
)
from sinch.domains.conversation.api.v1.exceptions import ConversationException


class DeleteMessageEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/messages/{message_id}"
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: DeleteMessageRequest):
        super(DeleteMessageEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_query_params(self) -> dict:
        path_params = self._get_path_params_from_url()
        return self.request_data.model_dump(
            exclude_none=True, by_alias=True, exclude=path_params
        )

    def handle_response(self, response: HTTPResponse):
        try:
            super(DeleteMessageEndpoint, self).handle_response(response)
        except ConversationException as e:
            raise ConversationException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )


class GetMessageEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/messages/{message_id}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: GetMessageRequest):
        super(GetMessageEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_query_params(self) -> dict:
        path_params = self._get_path_params_from_url()
        return self.request_data.model_dump(
            exclude_none=True, by_alias=True, exclude=path_params
        )

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


class UpdateMessageMetadataEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/messages/{message_id}"
    HTTP_METHOD = HTTPMethods.PATCH.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS = {"messages_source"}

    def __init__(
        self, project_id: str, request_data: UpdateMessageMetadataRequest
    ):
        super(UpdateMessageMetadataEndpoint, self).__init__(
            project_id, request_data
        )
        self.project_id = project_id
        self.request_data = request_data

    def build_query_params(self) -> dict:
        query_params = self.request_data.model_dump(
            include=self.QUERY_PARAM_FIELDS, exclude_none=True, by_alias=True
        )
        return query_params

    def request_body(self):
        path_params = self._get_path_params_from_url()
        exclude_set = path_params.union(self.QUERY_PARAM_FIELDS)
        request_data = self.request_data.model_dump(
            by_alias=True, exclude_none=True, exclude=exclude_set
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
