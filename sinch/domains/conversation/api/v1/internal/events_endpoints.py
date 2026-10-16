from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.conversation.api.v1.internal.base.conversation_endpoint import (
    ConversationEndpoint,
)
from sinch.domains.conversation.models.v1.events.internal.event_id_request import (
    EventIdRequest,
)
from sinch.domains.conversation.models.v1.events.internal.list_events_request import (
    ListEventsRequest,
)
from sinch.domains.conversation.models.v1.events.internal.list_events_response import (
    ListEventsResponse,
)
from sinch.domains.conversation.models.v1.events.internal.send_event_request import (
    SendEventRequest,
)
from sinch.domains.conversation.models.v1.events.response.conversation_event_response import (
    ConversationEventResponse,
)
from sinch.domains.conversation.models.v1.events.response.send_event_response import (
    SendEventResponse,
)


class SendEventEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/events:send"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: SendEventRequest,
        response_model=SendEventResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class GetEventEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/events/{event_id}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: EventIdRequest,
        response_model=ConversationEventResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class DeleteEventEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/events/{event_id}"
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: EventIdRequest):
        super().__init__(project_id, request_data)


class ListEventsEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/events"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS = {
        "conversation_id",
        "contact_id",
        "page_size",
        "page_token",
    }

    def __init__(
        self,
        project_id: str,
        request_data: ListEventsRequest,
        response_model=ListEventsResponse,
    ):
        super().__init__(project_id, request_data, response_model)
