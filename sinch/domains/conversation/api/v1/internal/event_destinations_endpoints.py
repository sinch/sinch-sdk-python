from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.internal.utils import query_params_to_comma_joined_lists
from sinch.domains.conversation.api.v1.internal.base.conversation_endpoint import (
    ConversationEndpoint,
)
from sinch.domains.conversation.models.v1.apps.internal.app_id_request import (
    AppIdRequest,
)
from sinch.domains.conversation.models.v1.event_destinations.internal.event_destination_id_request import (
    EventDestinationIdRequest,
)
from sinch.domains.conversation.models.v1.event_destinations.internal.list_event_destinations_response import (
    ListEventDestinationsResponse,
)
from sinch.domains.conversation.models.v1.event_destinations.request.create_event_destination_request import (
    CreateEventDestinationRequest,
)
from sinch.domains.conversation.models.v1.event_destinations.request.update_event_destination_request import (
    UpdateEventDestinationRequest,
)
from sinch.domains.conversation.models.v1.event_destinations.response.event_destination_response import (
    EventDestinationResponse,
)


class ListEventDestinationsEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/apps/{app_id}/webhooks"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: AppIdRequest,
        response_model=ListEventDestinationsResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class CreateEventDestinationEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/webhooks"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: CreateEventDestinationRequest,
        response_model=EventDestinationResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class GetEventDestinationEndpoint(ConversationEndpoint):
    ENDPOINT_URL = (
        "{origin}/v1/projects/{project_id}/webhooks/{event_destination_id}"
    )
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: EventDestinationIdRequest,
        response_model=EventDestinationResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class UpdateEventDestinationEndpoint(ConversationEndpoint):
    ENDPOINT_URL = (
        "{origin}/v1/projects/{project_id}/webhooks/{event_destination_id}"
    )
    HTTP_METHOD = HTTPMethods.PATCH.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS_EXPLODE_FALSE = {"update_mask"}

    def __init__(
        self,
        project_id: str,
        request_data: UpdateEventDestinationRequest,
        response_model=EventDestinationResponse,
    ):
        super().__init__(project_id, request_data, response_model)

    def build_query_params(self) -> dict:
        """update_mask lists which fields were set, it isn't a request_data field itself."""
        body_data = self._build_body_data()
        if not body_data:
            return {}
        return query_params_to_comma_joined_lists(
            {"update_mask": list(body_data.keys())}, ["update_mask"]
        )


class DeleteEventDestinationEndpoint(ConversationEndpoint):
    ENDPOINT_URL = (
        "{origin}/v1/projects/{project_id}/webhooks/{event_destination_id}"
    )
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self, project_id: str, request_data: EventDestinationIdRequest
    ):
        super().__init__(project_id, request_data)
