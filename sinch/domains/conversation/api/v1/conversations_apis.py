from datetime import datetime
from typing import Any, Dict, Literal, Optional, Union

from sinch.core.models.internal.utils import strip_unset
from sinch.core.pagination import Paginator, TokenBasedPaginator
from sinch.core.sentinel import UNSET, UnsetOr
from sinch.domains.conversation.api.v1.base.base_conversation import (
    BaseConversation,
)
from sinch.domains.conversation.api.v1.internal.utils import (
    validate_inject_message_body,
)
from sinch.domains.conversation.api.v1.internal.conversations_endpoints import (
    CreateConversationEndpoint,
    DeleteConversationEndpoint,
    GetConversationEndpoint,
    InjectEventEndpoint,
    InjectMessageEndpoint,
    ListConversationsEndpoint,
    ListRecentConversationsEndpoint,
    StopActiveConversationEndpoint,
    UpdateConversationEndpoint,
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
from sinch.domains.conversation.models.v1.conversations.response.recent_conversation_response import (
    RecentConversationResponse,
)
from sinch.domains.conversation.models.v1.events.types.app_event_dict import (
    AppEventDict,
)
from sinch.domains.conversation.models.v1.messages.types.app_message_dict import (
    AppMessageDict,
)
from sinch.domains.conversation.models.v1.messages.types.contact_message_dict import (
    ContactMessageDict,
)
from sinch.domains.conversation.models.v1.messages.types.conversation_direction_type import (
    ConversationDirectionType,
)
from sinch.domains.conversation.models.v1.messages.types.metadata_update_strategy_type import (
    MetadataUpdateStrategyType,
)
from sinch.domains.conversation.models.v1.types.channel_identity_dict import (
    ChannelIdentityDict,
)
from sinch.domains.conversation.models.v1.types.conversation_channel_type import (
    ConversationChannelType,
)
from sinch.domains.conversation.models.v1.types.processing_mode_type import (
    ProcessingModeType,
)


class Conversations(BaseConversation):
    def list(
        self,
        app_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        only_active: Optional[bool] = None,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
        active_channel: Optional[ConversationChannelType] = None,
        **kwargs,
    ) -> Paginator[ListConversationsResponse, ConversationResponse]:
        """
        This operation lists all conversations that are associated with an app and/or a contact.
        Note that either ``app_id`` or ``contact_id`` is required in order for the operation to
        function correctly.

        :param app_id: (optional) The ID of the app involved in the conversations.
        :type app_id: Optional[str]
        :param contact_id: (optional) The ID of the contact involved in the conversations.
        :type contact_id: Optional[str]
        :param only_active: (optional) Set to ``True`` to list only active conversations, ``False``
            to list only inactive ones.
        :type only_active: Optional[bool]
        :param page_size: (optional) The maximum number of conversations to fetch. The server
            default is 10 and the maximum is 20.
        :type page_size: Optional[int]
        :param page_token: (optional) Next page token previously returned if any.
        :type page_token: Optional[str]
        :param active_channel: (optional) Only fetch conversations from the ``active_channel``.
        :type active_channel: Optional[ConversationChannelType]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: A paginator for iterating through the conversations.
        :rtype: Paginator[ListConversationsResponse, ConversationResponse]

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        return TokenBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListConversationsEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListConversationsRequest(
                    app_id=app_id,
                    contact_id=contact_id,
                    only_active=only_active,
                    page_size=page_size,
                    page_token=page_token,
                    active_channel=active_channel,
                    **kwargs,
                ),
            ),
        )

    def create(
        self,
        app_id: str,
        contact_id: str,
        active: UnsetOr[Optional[bool]] = UNSET,
        active_channel: UnsetOr[Optional[ConversationChannelType]] = UNSET,
        metadata_json: UnsetOr[Optional[Dict[str, Any]]] = UNSET,
        correlation_id: UnsetOr[Optional[str]] = UNSET,
        **kwargs,
    ) -> ConversationResponse:
        """
        Creates a new empty conversation. In Conversation mode, it is generally not needed to
        create a conversation explicitly since sending or receiving a message automatically
        creates a new conversation if it does not already exist between the given app and
        contact. Creating empty conversation is useful if the metadata of the conversation
        should be populated when the first message in the conversation is a contact message or
        the first message in the conversation comes out-of-band and needs to be injected with
        InjectMessage endpoint.

        :param app_id: (required) The ID of the participating app.
        :type app_id: str
        :param contact_id: (required) The ID of the participating contact.
        :type contact_id: str
        :param active: (optional) Flag for whether this conversation is active.
        :type active: UnsetOr[Optional[bool]]
        :param active_channel: (optional) The active channel of the conversation.
        :type active_channel: UnsetOr[Optional[ConversationChannelType]]
        :param metadata_json: (optional) Arbitrary data set by the Conversation API clients.
            A valid JSON object.
        :type metadata_json: UnsetOr[Optional[Dict[str, Any]]]
        :param correlation_id: (optional) Arbitrary correlation ID related to the MT message
            set by the Conversation API user.
        :type correlation_id: UnsetOr[Optional[str]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: The created conversation.
        :rtype: ConversationResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = CreateConversationRequest(
            app_id=app_id,
            contact_id=contact_id,
            **strip_unset(
                {
                    "active": active,
                    "active_channel": active_channel,
                    "metadata_json": metadata_json,
                    "correlation_id": correlation_id,
                }
            ),
            **kwargs,
        )
        return self._request(CreateConversationEndpoint, request_data)

    def get(self, conversation_id: str, **kwargs) -> ConversationResponse:
        """
        Retrieves a conversation by id. A conversation has two participating entities, an app
        and a contact.

        :param conversation_id: (required) The unique ID of the conversation.
        :type conversation_id: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: The conversation.
        :rtype: ConversationResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = ConversationIdRequest(
            conversation_id=conversation_id, **kwargs
        )
        return self._request(GetConversationEndpoint, request_data)

    def delete(self, conversation_id: str, **kwargs) -> None:
        """
        Deletes a conversation together with all the messages sent as part of the conversation.

        :param conversation_id: (required) The unique ID of the conversation.
        :type conversation_id: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: None
        :rtype: None

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = ConversationIdRequest(
            conversation_id=conversation_id, **kwargs
        )
        return self._request(DeleteConversationEndpoint, request_data)

    def update(
        self,
        conversation_id: str,
        active: UnsetOr[Optional[bool]] = UNSET,
        active_channel: UnsetOr[Optional[ConversationChannelType]] = UNSET,
        app_id: UnsetOr[Optional[str]] = UNSET,
        contact_id: UnsetOr[Optional[str]] = UNSET,
        metadata_json: UnsetOr[Optional[Dict[str, Any]]] = UNSET,
        correlation_id: UnsetOr[Optional[str]] = UNSET,
        metadata_update_strategy: Optional[MetadataUpdateStrategyType] = None,
        **kwargs,
    ) -> ConversationResponse:
        """
        This operation updates a conversation which can, for instance, be used to update the
        metadata associated with a conversation.

        Omitted parameters are left untouched on the server; passing ``None``
        explicitly clears the field.

        :param conversation_id: (required) The unique ID of the conversation.
        :type conversation_id: str
        :param active: (optional) Flag for whether this conversation is active.
        :type active: UnsetOr[Optional[bool]]
        :param active_channel: (optional) The active channel of the conversation.
        :type active_channel: UnsetOr[Optional[ConversationChannelType]]
        :param app_id: (optional) The ID of the participating app.
        :type app_id: UnsetOr[Optional[str]]
        :param contact_id: (optional) The ID of the participating contact.
        :type contact_id: UnsetOr[Optional[str]]
        :param metadata_json: (optional) Arbitrary data set by the Conversation API clients.
            A valid JSON object.
        :type metadata_json: UnsetOr[Optional[Dict[str, Any]]]
        :param correlation_id: (optional) Arbitrary correlation ID related to the MT message
            set by the Conversation API user.
        :type correlation_id: UnsetOr[Optional[str]]
        :param metadata_update_strategy: (optional) Update strategy for the
            ``conversation_metadata`` field. The server default is ``REPLACE``.
        :type metadata_update_strategy: Optional[MetadataUpdateStrategyType]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: The updated conversation.
        :rtype: ConversationResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = UpdateConversationRequest(
            conversation_id=conversation_id,
            metadata_update_strategy=metadata_update_strategy,
            **strip_unset(
                {
                    "active": active,
                    "active_channel": active_channel,
                    "app_id": app_id,
                    "contact_id": contact_id,
                    "metadata_json": metadata_json,
                    "correlation_id": correlation_id,
                }
            ),
            **kwargs,
        )
        return self._request(UpdateConversationEndpoint, request_data)

    def list_recent(
        self,
        app_id: str,
        only_active: Optional[bool] = None,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
        order: Optional[Union[Literal["ASC", "DESC"], str]] = None,
        **kwargs,
    ) -> Paginator[
        ListRecentConversationsResponse, RecentConversationResponse
    ]:
        """
        This operation lists conversations and their most recent message, ordered by when the
        most recent message was sent for that conversation.

        :param app_id: (required) The application ID.
        :type app_id: str
        :param only_active: (optional) ``True`` if only active conversations should be listed.
            The server default is ``False``.
        :type only_active: Optional[bool]
        :param page_size: (optional) The maximum number of conversations to fetch. The server
            default is 10 and the maximum value is 50.
        :type page_size: Optional[int]
        :param page_token: (optional) Next page token previously returned if any.
        :type page_token: Optional[str]
        :param order: (optional) Whether to sort conversations by newest message first
            (``DESC``) or oldest (``ASC``). The server default is ``DESC``.
        :type order: Optional[Union[Literal["ASC", "DESC"], str]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: A paginator for iterating through the recent conversations.
        :rtype: Paginator[ListRecentConversationsResponse, RecentConversationResponse]

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        return TokenBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListRecentConversationsEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListRecentConversationsRequest(
                    app_id=app_id,
                    only_active=only_active,
                    page_size=page_size,
                    page_token=page_token,
                    order=order,
                    **kwargs,
                ),
            ),
        )

    def stop_active(self, conversation_id: str, **kwargs) -> None:
        """
        This operation stops the referenced conversation, if the conversation is still active.
        In Conversation mode, a new conversation will be created if a new message is exchanged
        between the app or contact that was part of the stopped conversation.

        :param conversation_id: (required) The unique ID of the conversation.
        :type conversation_id: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: None
        :rtype: None

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = ConversationIdRequest(
            conversation_id=conversation_id, **kwargs
        )
        return self._request(StopActiveConversationEndpoint, request_data)

    def inject_message(
        self,
        conversation_id: str,
        contact_id: str,
        channel_identity: ChannelIdentityDict,
        direction: ConversationDirectionType,
        accept_time: datetime,
        app_message: UnsetOr[AppMessageDict] = UNSET,
        contact_message: UnsetOr[ContactMessageDict] = UNSET,
        sender_id: UnsetOr[Optional[str]] = UNSET,
        processing_mode: UnsetOr[Optional[ProcessingModeType]] = UNSET,
        metadata: UnsetOr[Optional[str]] = UNSET,
        **kwargs,
    ) -> None:
        """
        This operation injects a conversation message in to a specific conversation.

        Set exactly one of ``app_message`` or ``contact_message``; otherwise a
        ``ValueError`` is raised.

        :param conversation_id: (required) The ID of the conversation.
        :type conversation_id: str
        :param contact_id: (required) The ID of the contact registered in the conversation
            provided.
        :type contact_id: str
        :param channel_identity: (required) The channel identity of the contact.
        :type channel_identity: ChannelIdentityDict
        :param direction: (required) The direction of the message flow: ``TO_APP`` or
            ``TO_CONTACT``.
        :type direction: ConversationDirectionType
        :param accept_time: (required) The processed time of the message in UTC timezone. Must
            be less than current_time and greater than (current_time - 30 days).
        :type accept_time: datetime
        :param app_message: (optional) A message originating from a Conversation API app.
        :type app_message: UnsetOr[AppMessageDict]
        :param contact_message: (optional) A message originating from a contact.
        :type contact_message: UnsetOr[ContactMessageDict]
        :param sender_id: (optional) For Contact Messages (MO messages), the sender ID
            represents the recipient to which the message was sent.
        :type sender_id: UnsetOr[Optional[str]]
        :param processing_mode: (optional) Whether or not Conversation API should store
            contacts and conversations for the app.
        :type processing_mode: UnsetOr[Optional[ProcessingModeType]]
        :param metadata: (optional) Metadata associated with the contact. Up to 1024 characters
            long.
        :type metadata: UnsetOr[Optional[str]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: None
        :rtype: None

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        validate_inject_message_body(app_message, contact_message)
        request_data = InjectMessageRequest(
            conversation_id=conversation_id,
            contact_id=contact_id,
            channel_identity=channel_identity,
            direction=direction,
            accept_time=accept_time,
            **strip_unset(
                {
                    "app_message": app_message,
                    "contact_message": contact_message,
                    "sender_id": sender_id,
                    "processing_mode": processing_mode,
                    "metadata": metadata,
                }
            ),
            **kwargs,
        )
        return self._request(InjectMessageEndpoint, request_data)

    def inject_event(
        self,
        conversation_id: str,
        app_event: AppEventDict,
        accept_time: datetime,
        contact_id: UnsetOr[Optional[str]] = UNSET,
        channel_identity: UnsetOr[Optional[ChannelIdentityDict]] = UNSET,
        processing_mode: UnsetOr[Optional[ProcessingModeType]] = UNSET,
        **kwargs,
    ) -> InjectEventResponse:
        """
        This operation injects a conversation event in to a specific conversation. It only
        supports injecting App events in ``CONVERSATION`` mode.

        :param conversation_id: (required) The unique ID of the conversation.
        :type conversation_id: str
        :param app_event: (required) The event originating from an app. Set exactly one event
            type key.
        :type app_event: AppEventDict
        :param accept_time: (required) The processed time of the event in UTC timezone. Must be
            less than current_time and greater than (current_time - 30 days).
        :type accept_time: datetime
        :param contact_id: (optional) The ID of the contact.
        :type contact_id: UnsetOr[Optional[str]]
        :param channel_identity: (optional) The channel identity of the contact.
        :type channel_identity: UnsetOr[Optional[ChannelIdentityDict]]
        :param processing_mode: (optional) Whether or not Conversation API should store
            contacts and conversations for the app.
        :type processing_mode: UnsetOr[Optional[ProcessingModeType]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: The ID and accepted time of the injected event.
        :rtype: InjectEventResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = InjectEventRequest(
            conversation_id=conversation_id,
            app_event=app_event,
            accept_time=accept_time,
            **strip_unset(
                {
                    "contact_id": contact_id,
                    "channel_identity": channel_identity,
                    "processing_mode": processing_mode,
                }
            ),
            **kwargs,
        )
        return self._request(InjectEventEndpoint, request_data)
