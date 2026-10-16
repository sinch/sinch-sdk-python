from typing import List, Optional

from sinch.core.models.internal.utils import strip_unset
from sinch.core.pagination import Paginator, TokenBasedPaginator
from sinch.core.sentinel import UNSET, UnsetOr
from sinch.domains.conversation.api.v1.base import BaseConversation
from sinch.domains.conversation.api.v1.internal.events_endpoints import (
    DeleteEventEndpoint,
    GetEventEndpoint,
    ListEventsEndpoint,
    SendEventEndpoint,
)
from sinch.domains.conversation.api.v1.internal.utils import (
    build_recipient_dict,
    coerce_recipient,
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
from sinch.domains.conversation.models.v1.events.types import AppEventDict
from sinch.domains.conversation.models.v1.messages.types import (
    ChannelRecipientIdentityDict,
    MessageQueueType,
)
from sinch.domains.conversation.models.v1.types import ConversationChannelType


class Events(BaseConversation):
    def send(
        self,
        app_id: str,
        event: AppEventDict,
        contact_id: Optional[str] = None,
        recipient_identities: Optional[
            List[ChannelRecipientIdentityDict]
        ] = None,
        event_destination_target: UnsetOr[Optional[str]] = UNSET,
        channel_priority_order: UnsetOr[
            Optional[List[ConversationChannelType]]
        ] = UNSET,
        event_metadata: UnsetOr[Optional[str]] = UNSET,
        queue: UnsetOr[Optional[MessageQueueType]] = UNSET,
        **kwargs,
    ) -> SendEventResponse:
        """
        Sends an event to the referenced contact from the referenced app.
        Note that this operation enqueues the event in a queue so a successful
        response only indicates that the event has been queued.

        :param app_id: The ID of the app sending the event.
        :type app_id: str
        :param event: The event to be sent. Set exactly one event type key.
        :type event: AppEventDict
        :param contact_id: The ID of the recipient contact. Either contact_id or recipient_identities must be provided.
        :type contact_id: Optional[str]
        :param recipient_identities: Channel identities of the recipient. Either contact_id or recipient_identities must be provided.
        :type recipient_identities: Optional[List[ChannelRecipientIdentityDict]]
        :param event_destination_target: Overwrites the default event destination target for delivery receipts for this event.
        :type event_destination_target: UnsetOr[Optional[str]]
        :param channel_priority_order: Optional. A single element array that dictates on what channel should the Conversation API try to send the event.
        :type channel_priority_order: UnsetOr[Optional[List[ConversationChannelType]]]
        :param event_metadata: Optional. Metadata that should be associated to the event.
        :type event_metadata: UnsetOr[Optional[str]]
        :param queue: Select the priority type for the event.
        :type queue: UnsetOr[Optional[MessageQueueType]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: The accepted event.
        :rtype: SendEventResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        recipient = coerce_recipient(
            build_recipient_dict(
                contact_id=contact_id,
                recipient_identities=recipient_identities,
            )
        )
        request_data = SendEventRequest(
            app_id=app_id,
            event=event,
            recipient=recipient,
            **strip_unset(
                {
                    "event_destination_target": event_destination_target,
                    "channel_priority_order": channel_priority_order,
                    "event_metadata": event_metadata,
                    "queue": queue,
                }
            ),
            **kwargs,
        )
        return self._request(SendEventEndpoint, request_data)

    def get(self, event_id: str, **kwargs) -> ConversationEventResponse:
        """
        Get event from ID.

        :param event_id: The unique ID of the event.
        :type event_id: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: The event.
        :rtype: ConversationEventResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = EventIdRequest(event_id=event_id, **kwargs)
        return self._request(GetEventEndpoint, request_data)

    def delete(self, event_id: str, **kwargs) -> None:
        """
        Delete a specific event by its ID.

        :param event_id: The unique ID of the event.
        :type event_id: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: None
        :rtype: None

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = EventIdRequest(event_id=event_id, **kwargs)
        return self._request(DeleteEventEndpoint, request_data)

    def list(
        self,
        conversation_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
        **kwargs,
    ) -> Paginator[ListEventsResponse, ConversationEventResponse]:
        """
        List all events in a project.

        :param conversation_id: Resource name (id) of the conversation. One of conversation_id or contact_id needs to be present.
        :type conversation_id: Optional[str]
        :param contact_id: Resource name (id) of the contact. One of conversation_id or contact_id needs to be present.
        :type contact_id: Optional[str]
        :param page_size: Maximum number of events to fetch. Defaults to 10 and the maximum is 20.
        :type page_size: Optional[int]
        :param page_token: Next page token previously returned if any.
        :type page_token: Optional[str]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: A paginator for iterating through the events.
        :rtype: Paginator[ListEventsResponse, ConversationEventResponse]

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        return TokenBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListEventsEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListEventsRequest(
                    conversation_id=conversation_id,
                    contact_id=contact_id,
                    page_size=page_size,
                    page_token=page_token,
                    **kwargs,
                ),
            ),
        )
