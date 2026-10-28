from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.conversation.api.v1.internal.base.conversation_endpoint import (
    ConversationEndpoint,
)
from sinch.domains.conversation.models.v1.conversations.internal.conversation_id_request import (
    ConversationIdRequest,
)
from sinch.domains.conversation.models.v1.conversations.internal.create_conversation_request import (
    CreateConversationRequest,
)
from sinch.domains.conversation.models.v1.conversations.internal.inject_event_request import (
    InjectEventRequest,
)
from sinch.domains.conversation.models.v1.conversations.internal.inject_message_request import (
    InjectMessageRequest,
)
from sinch.domains.conversation.models.v1.conversations.internal.list_conversations_request import (
    ListConversationsRequest,
)
from sinch.domains.conversation.models.v1.conversations.internal.list_conversations_response import (
    ListConversationsResponse,
)
from sinch.domains.conversation.models.v1.conversations.internal.list_recent_conversations_request import (
    ListRecentConversationsRequest,
)
from sinch.domains.conversation.models.v1.conversations.internal.list_recent_conversations_response import (
    ListRecentConversationsResponse,
)
from sinch.domains.conversation.models.v1.conversations.internal.update_conversation_request import (
    UpdateConversationRequest,
)
from sinch.domains.conversation.models.v1.conversations.response.conversation_response import (
    ConversationResponse,
)
from sinch.domains.conversation.models.v1.conversations.response.inject_event_response import (
    InjectEventResponse,
)


class ListConversationsEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/conversations"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS = {
        "app_id",
        "contact_id",
        "only_active",
        "page_size",
        "page_token",
        "active_channel",
    }

    def __init__(
        self,
        project_id: str,
        request_data: ListConversationsRequest,
        response_model=ListConversationsResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class CreateConversationEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/conversations"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: CreateConversationRequest,
        response_model=ConversationResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class GetConversationEndpoint(ConversationEndpoint):
    ENDPOINT_URL = (
        "{origin}/v1/projects/{project_id}/conversations/{conversation_id}"
    )
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: ConversationIdRequest,
        response_model=ConversationResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class DeleteConversationEndpoint(ConversationEndpoint):
    ENDPOINT_URL = (
        "{origin}/v1/projects/{project_id}/conversations/{conversation_id}"
    )
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: ConversationIdRequest):
        super().__init__(project_id, request_data)


class UpdateConversationEndpoint(ConversationEndpoint):
    ENDPOINT_URL = (
        "{origin}/v1/projects/{project_id}/conversations/{conversation_id}"
    )
    HTTP_METHOD = HTTPMethods.PATCH.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS = {"metadata_update_strategy"}

    def __init__(
        self,
        project_id: str,
        request_data: UpdateConversationRequest,
        response_model=ConversationResponse,
    ):
        super().__init__(project_id, request_data, response_model)

    def build_query_params(self) -> dict:
        """update_mask lists which fields were set, it isn't a request_data field itself."""
        query_params = super().build_query_params()
        body_data = self._build_body_data()
        if body_data:
            query_params["update_mask"] = ",".join(body_data.keys())
        return query_params


class ListRecentConversationsEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/conversations:recent"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS = {
        "app_id",
        "only_active",
        "page_size",
        "page_token",
        "order",
    }

    def __init__(
        self,
        project_id: str,
        request_data: ListRecentConversationsRequest,
        response_model=ListRecentConversationsResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class StopActiveConversationEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/conversations/{conversation_id}:stop"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: ConversationIdRequest):
        super().__init__(project_id, request_data)


class InjectMessageEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/conversations/{conversation_id}:inject-message"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: InjectMessageRequest):
        super().__init__(project_id, request_data)


class InjectEventEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/conversations/{conversation_id}:inject-event"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: InjectEventRequest,
        response_model=InjectEventResponse,
    ):
        super().__init__(project_id, request_data, response_model)
