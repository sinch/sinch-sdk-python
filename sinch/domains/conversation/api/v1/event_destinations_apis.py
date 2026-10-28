from typing import List, Optional

from sinch.core.models.internal.utils import strip_unset
from sinch.core.pagination import Paginator, TokenBasedPaginator
from sinch.core.sentinel import UNSET, UnsetOr
from sinch.domains.conversation.api.v1.base import BaseConversation
from sinch.domains.conversation.api.v1.internal.event_destinations_endpoints import (
    CreateEventDestinationEndpoint,
    DeleteEventDestinationEndpoint,
    GetEventDestinationEndpoint,
    ListEventDestinationsEndpoint,
    UpdateEventDestinationEndpoint,
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
from sinch.domains.conversation.models.v1.event_destinations.types import (
    ClientCredentialsDict,
    EventDestinationTargetType,
    EventDestinationTriggerType,
)


class EventDestinations(BaseConversation):
    def create(
        self,
        app_id: str,
        target: str,
        client_credentials: UnsetOr[Optional[ClientCredentialsDict]] = UNSET,
        secret: UnsetOr[Optional[str]] = UNSET,
        target_type: UnsetOr[Optional[EventDestinationTargetType]] = UNSET,
        triggers: UnsetOr[Optional[List[EventDestinationTriggerType]]] = UNSET,
        **kwargs,
    ) -> EventDestinationResponse:
        """
        Creates an event destination for receiving events on specific triggers.
        You can create up to 5 event destinations per app.

        :param app_id: The app that this event destination belongs to.
        :type app_id: str
        :param target: The target url where events should be sent to.
            Maximum URL length is 742. The conversation-api.*.sinch.com subdomains are forbidden.
        :type target: str
        :param client_credentials: Optional. Used for OAuth2 authentication.
        :type client_credentials: UnsetOr[Optional[ClientCredentialsDict]]
        :param secret: Optional secret used to sign the contents of the events.
        :type secret: UnsetOr[Optional[str]]
        :param target_type: The type of the target.
        :type target_type: UnsetOr[Optional[EventDestinationTargetType]]
        :param triggers: The triggers that result in an event being sent to the target.
        :type triggers: UnsetOr[Optional[List[EventDestinationTriggerType]]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: The created event destination.
        :rtype: EventDestinationResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = CreateEventDestinationRequest(
            app_id=app_id,
            target=target,
            **strip_unset(
                {
                    "client_credentials": client_credentials,
                    "secret": secret,
                    "target_type": target_type,
                    "triggers": triggers,
                }
            ),
            **kwargs,
        )
        return self._request(CreateEventDestinationEndpoint, request_data)

    def list(
        self, app_id: str, **kwargs
    ) -> Paginator[ListEventDestinationsResponse, EventDestinationResponse]:
        """
        List all event destinations for a given app as specified by the App ID.

        :param app_id: The ID of the app.
        :type app_id: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: A paginator for iterating through the event destinations.
        :rtype: Paginator[ListEventDestinationsResponse, EventDestinationResponse]

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        return TokenBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListEventDestinationsEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=AppIdRequest(app_id=app_id, **kwargs),
            ),
        )

    def get(
        self, event_destination_id: str, **kwargs
    ) -> EventDestinationResponse:
        """
        Get an event destination as specified by the event destination ID.

        :param event_destination_id: The ID of the event destination to retrieve.
        :type event_destination_id: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: The event destination details.
        :rtype: EventDestinationResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = EventDestinationIdRequest(
            event_destination_id=event_destination_id, **kwargs
        )
        return self._request(GetEventDestinationEndpoint, request_data)

    def update(
        self,
        event_destination_id: str,
        app_id: UnsetOr[str] = UNSET,
        target: UnsetOr[str] = UNSET,
        client_credentials: UnsetOr[Optional[ClientCredentialsDict]] = UNSET,
        secret: UnsetOr[Optional[str]] = UNSET,
        target_type: UnsetOr[Optional[EventDestinationTargetType]] = UNSET,
        triggers: UnsetOr[Optional[List[EventDestinationTriggerType]]] = UNSET,
        **kwargs,
    ) -> EventDestinationResponse:
        """
        Updates an existing event destination as specified by the event destination ID.

        Omitted parameters are left untouched on the server; passing ``None``
        explicitly clears the field.

        :param event_destination_id: The ID of the event destination to update.
        :type event_destination_id: str
        :param app_id: The app that this event destination belongs to.
        :type app_id: UnsetOr[Optional[str]]
        :param target: The target url where events should be sent to.
        :type target: UnsetOr[Optional[str]]
        :param client_credentials: Optional. Used for OAuth2 authentication.
        :type client_credentials: UnsetOr[Optional[ClientCredentialsDict]]
        :param secret: Optional secret used to sign the contents of the events.
        :type secret: UnsetOr[Optional[str]]
        :param target_type: The type of the target.
        :type target_type: UnsetOr[Optional[EventDestinationTargetType]]
        :param triggers: The triggers that result in an event being sent to the target.
        :type triggers: UnsetOr[Optional[List[EventDestinationTriggerType]]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: The updated event destination.
        :rtype: EventDestinationResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = UpdateEventDestinationRequest(
            event_destination_id=event_destination_id,
            **strip_unset(
                {
                    "app_id": app_id,
                    "target": target,
                    "client_credentials": client_credentials,
                    "secret": secret,
                    "target_type": target_type,
                    "triggers": triggers,
                }
            ),
            **kwargs,
        )
        return self._request(UpdateEventDestinationEndpoint, request_data)

    def delete(self, event_destination_id: str, **kwargs) -> None:
        """
        Deletes an event destination as specified by the event destination ID.

        :param event_destination_id: The ID of the event destination to delete.
        :type event_destination_id: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: None
        :rtype: None

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = EventDestinationIdRequest(
            event_destination_id=event_destination_id, **kwargs
        )
        return self._request(DeleteEventDestinationEndpoint, request_data)
