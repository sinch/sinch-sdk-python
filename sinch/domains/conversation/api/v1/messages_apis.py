from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from sinch.core.pagination import Paginator, TokenBasedPaginator
from sinch.domains.conversation.models.v1.messages.internal.request import (
    ListMessagesRequest,
    MessageIdRequest,
    UpdateMessageMetadataRequest,
    SendMessageRequest,
    SendMessageRequestBody,
)
from sinch.domains.conversation.models.v1.messages.response.types import (
    ConversationMessageResponse,
    SendMessageResponse,
)
from sinch.domains.conversation.models.v1.messages.types import (
    ConversationChannelType,
    ConversationDirectionType,
    ConversationMessagesViewType,
    MessageContentType,
    MessageQueueType,
    MessagesSourceType,
    MetadataUpdateStrategyType,
    ProcessingStrategyType,
    CardMessageDict,
    CarouselMessageDict,
    ChoiceMessageDict,
    ContactInfoMessageDict,
    ListMessageDict,
    LocationMessageDict,
    MediaPropertiesDict,
    TemplateMessageDict,
    ChannelRecipientIdentityDict,
    SendMessageRequestBodyDict,
)
from sinch.domains.conversation.models.v1.messages.categories.text import (
    TextMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.card import (
    CardMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.carousel import (
    CarouselMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.choice import (
    ChoiceMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.contactinfo import (
    ContactInfoMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.list import (
    ListMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.location import (
    LocationMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.media import (
    MediaProperties,
)
from sinch.domains.conversation.models.v1.messages.categories.template import (
    TemplateMessage,
)
from sinch.domains.conversation.api.v1.internal import (
    DeleteMessageEndpoint,
    GetMessageEndpoint,
    ListMessagesEndpoint,
    UpdateMessageMetadataEndpoint,
    SendMessageEndpoint,
)
from sinch.domains.conversation.api.v1.base import BaseConversation
from sinch.domains.conversation.api.v1.utils import (
    build_recipient_dict,
    coerce_recipient,
    split_send_kwargs,
)


class Messages(BaseConversation):
    def delete(
        self,
        message_id: str,
        messages_source: Optional[MessagesSourceType] = None,
        **kwargs,
    ) -> None:
        """
        Delete a specific message by its ID. Note that this operation deletes the message from Conversation API storage;
            this operation does not affect messages already delivered to recipients' handsets. Also note that removing all
            messages of a conversation will not automatically delete the
            conversation.

        :param message_id: The unique ID of the message. (required)
        :type message_id: str
        :param messages_source: Specifies the message source for which the request will be processed. Used for
            operations on messages in Dispatch Mode. Defaults to `CONVERSATION_SOURCE` when not specified. For more information,
            see [Processing Modes](https://developers.sinch.com/docs/conversation/processing-modes/).
            (optional)
        :type messages_source: Optional[MessagesSource]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: None
        :rtype: None

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = MessageIdRequest(
            message_id=message_id, messages_source=messages_source, **kwargs
        )
        return self._request(DeleteMessageEndpoint, request_data)

    def get(
        self,
        message_id: str,
        messages_source: Optional[MessagesSourceType] = None,
        **kwargs,
    ) -> ConversationMessageResponse:
        """
        Retrieves a specific message by its ID.

        :param message_id: The unique ID of the message. (required)
        :type message_id: str
        :param messages_source: Specifies the message source for which the request will be processed. Used for
            operations on messages in Dispatch Mode. Defaults to `CONVERSATION_SOURCE` when not specified. For more information,
            see [Processing Modes](https://developers.sinch.com/docs/conversation/processing-modes/).
            (optional)
        :type messages_source: Optional[MessagesSource]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: ConversationMessageResponse
        :rtype: ConversationMessageResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = MessageIdRequest(
            message_id=message_id, messages_source=messages_source, **kwargs
        )
        return self._request(GetMessageEndpoint, request_data)

    def list(
        self,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
        conversation_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        app_id: Optional[str] = None,
        channel_identity: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        view: Optional[ConversationMessagesViewType] = None,
        messages_source: Optional[MessagesSourceType] = None,
        only_recipient_originated: Optional[bool] = None,
        channel: Optional[ConversationChannelType] = None,
        direction: Optional[ConversationDirectionType] = None,
        **kwargs,
    ) -> Paginator[ConversationMessageResponse]:
        """
        List messages sent or received via particular Processing Modes.
        The messages are ordered by their accept_time property in descending order.

        :param page_size: Maximum number of messages to fetch. Defaults to 10, maximum is 1000.
        :type page_size: Optional[int]
        :param page_token: Next page token previously returned if any.
        :type page_token: Optional[str]
        :param conversation_id: Filter messages by conversation ID.
        :type conversation_id: Optional[str]
        :param contact_id: Filter messages by contact ID.
        :type contact_id: Optional[str]
        :param app_id: Filter messages by app ID.
        :type app_id: Optional[str]
        :param channel_identity: Channel identity of the contact.
        :type channel_identity: Optional[str]
        :param start_time: Filter messages with accept_time after this timestamp.
        :type start_time: Optional[datetime]
        :param end_time: Filter messages with accept_time before this timestamp.
        :type end_time: Optional[datetime]
        :param view: Messages view type. WITH_METADATA or WITHOUT_METADATA.
        :type view: Optional[ConversationMessagesViewType]
        :param messages_source: Specifies the message source for the request.
        :type messages_source: Optional[MessagesSourceType]
        :param only_recipient_originated: Only fetch recipient-originated messages.
        :type only_recipient_originated: Optional[bool]
        :param channel: Only fetch messages from the specified channel.
        :type channel: Optional[ConversationChannelType]
        :param direction: Only fetch messages with the specified direction. TO_APP or TO_CONTACT.
        :type direction: Optional[ConversationDirectionType]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: TokenBasedPaginator with ConversationMessageResponse items
        :rtype: Paginator[ConversationMessageResponse]

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        return TokenBasedPaginator(
            sinch=self._sinch,
            endpoint=ListMessagesEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListMessagesRequest(
                    page_size=page_size,
                    page_token=page_token,
                    conversation_id=conversation_id,
                    contact_id=contact_id,
                    app_id=app_id,
                    channel_identity=channel_identity,
                    start_time=start_time,
                    end_time=end_time,
                    view=view,
                    messages_source=messages_source,
                    only_recipient_originated=only_recipient_originated,
                    channel=channel,
                    direction=direction,
                    **kwargs,
                ),
            ),
        )

    def update(
        self,
        message_id: str,
        metadata: str,
        messages_source: Optional[MessagesSourceType] = None,
        **kwargs,
    ) -> ConversationMessageResponse:
        """
        Update a specific message metadata by its ID.

        :param message_id: The unique ID of the message. (required)
        :type message_id: str
        :param metadata: Metadata that should be associated with the message. (required)
        :type metadata: str
        :param messages_source: Specifies the message source for which the request will be processed. Used for
            operations on messages in Dispatch Mode. Defaults to `CONVERSATION_SOURCE` when not specified. For more information,
            see [Processing Modes](https://developers.sinch.com/docs/conversation/processing-modes/).
            (optional)
        :type messages_source: Optional[MessagesSource]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: ConversationMessageResponse
        :rtype: ConversationMessageResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = UpdateMessageMetadataRequest(
            message_id=message_id,
            metadata=metadata,
            messages_source=messages_source,
            **kwargs,
        )
        return self._request(UpdateMessageMetadataEndpoint, request_data)

    def _send_message_variant(
        self,
        app_id: str,
        contact_id: Optional[str],
        recipient_identities: Optional[List[ChannelRecipientIdentityDict]],
        message_field: str,
        message: object,
        message_cls: type,
        ttl: Optional[Union[str, int]] = None,
        callback_url: Optional[str] = None,
        channel_priority_order: Optional[List[ConversationChannelType]] = None,
        channel_properties: Optional[Dict[str, str]] = None,
        message_metadata: Optional[str] = None,
        conversation_metadata: Optional[Dict[str, Any]] = None,
        queue: Optional[MessageQueueType] = None,
        processing_strategy: Optional[ProcessingStrategyType] = None,
        correlation_id: Optional[str] = None,
        conversation_metadata_update_strategy: Optional[
            MetadataUpdateStrategyType
        ] = None,
        message_content_type: Optional[MessageContentType] = None,
        **kwargs,
    ) -> SendMessageResponse:
        """
        - Builds Recipient Dictionary from contact_id or recipient_identities
        - Normalizes recipient dict -> Recipient model
        - Normalizes message dict -> message_cls(**message)
        - Builds SendMessageRequest(message=..., recipient=..., app_id=...) and sends the request
        """
        recipient_dict = build_recipient_dict(
            contact_id=contact_id, recipient_identities=recipient_identities
        )
        recipient_model = coerce_recipient(recipient_dict)
        if isinstance(message, dict):
            message = message_cls(**message)

        message_kwargs, request_kwargs = split_send_kwargs(kwargs)
        send_message_request_body = SendMessageRequestBody(
            **{message_field: message},
            **message_kwargs,
        )
        request_data = SendMessageRequest(
            app_id=app_id,
            recipient=recipient_model,
            message=send_message_request_body,
            ttl=ttl,
            callback_url=callback_url,
            channel_priority_order=channel_priority_order,
            channel_properties=channel_properties,
            message_metadata=message_metadata,
            conversation_metadata=conversation_metadata,
            queue=queue,
            processing_strategy=processing_strategy,
            correlation_id=correlation_id,
            conversation_metadata_update_strategy=conversation_metadata_update_strategy,
            message_content_type=message_content_type,
            **request_kwargs,
        )
        return self._request(SendMessageEndpoint, request_data)

    def send(
        self,
        app_id: str,
        message: Union[SendMessageRequestBodyDict, dict],
        contact_id: Optional[str] = None,
        recipient_identities: Optional[
            List[ChannelRecipientIdentityDict]
        ] = None,
        ttl: Optional[Union[str, int]] = None,
        callback_url: Optional[str] = None,
        channel_priority_order: Optional[List[ConversationChannelType]] = None,
        channel_properties: Optional[Dict[str, str]] = None,
        message_metadata: Optional[str] = None,
        conversation_metadata: Optional[Dict[str, Any]] = None,
        queue: Optional[MessageQueueType] = None,
        processing_strategy: Optional[ProcessingStrategyType] = None,
        correlation_id: Optional[str] = None,
        conversation_metadata_update_strategy: Optional[
            MetadataUpdateStrategyType
        ] = None,
        message_content_type: Optional[MessageContentType] = None,
        **kwargs,
    ) -> SendMessageResponse:
        """
        Send a message from a Conversation app to a contact associated with that app.
        If the recipient is not associated with an existing contact, a new contact will be created.
        The message is added to the active conversation with the contact if a conversation already exists.
        If no active conversation exists a new one is started automatically.

        :param app_id: The ID of the Conversation API app sending the message.
        :type app_id: str
        :param message: The message content to send. Can be a SendMessageRequestBodyDict or a dict.
        :type message: Union[SendMessageRequestBodyDict, dict]
        :param contact_id: The contact ID of the recipient. Either contact_id or recipient_identities must be provided.
        :type contact_id: Optional[str]
        :param recipient_identities: List of channel identities for the recipient. Either contact_id or recipient_identities must be provided.
        :type recipient_identities: Optional[List[ChannelRecipientIdentityDict]]
        :param ttl: The timeout allotted for sending the message. Can be seconds (int) or a string like '10s'.
        :type ttl: Optional[Union[str, int]]
        :param callback_url: Overwrites the default callback url for delivery receipts for this message.
        :type callback_url: Optional[str]
        :param channel_priority_order: Explicitly define the channels and order in which they are tried when sending the message.
        :type channel_priority_order: Optional[List[ConversationChannelType]]
        :param channel_properties: Channel-specific properties. The key in the map must point to a valid channel property key.
        :type channel_properties: Optional[Dict[str, str]]
        :param message_metadata: Metadata that should be associated with the message. Up to 1024 characters long.
        :type message_metadata: Optional[str]
        :param conversation_metadata: Metadata that will be associated with the conversation. Up to 2048 characters long.
        :type conversation_metadata: Optional[Dict[str, Any]]
        :param queue: Select the priority type for the message. Can be 'NORMAL_PRIORITY' or 'HIGH_PRIORITY'.
        :type queue: Optional[MessageQueueType]
        :param processing_strategy: Overrides the app's Processing Mode. Can be 'DEFAULT' or 'DISPATCH_ONLY'.
        :type processing_strategy: Optional[ProcessingStrategyType]
        :param correlation_id: An arbitrary identifier that will be propagated to callbacks related to this message. Up to 128 characters long.
        :type correlation_id: Optional[str]
        :param conversation_metadata_update_strategy: Update strategy for the conversation_metadata field. Can be 'REPLACE' or 'MERGE_PATCH'.
        :type conversation_metadata_update_strategy: Optional[MetadataUpdateStrategyType]
        :param message_content_type: Classifies the message content for use with consent management. Can be 'CONTENT_UNKNOWN', 'CONTENT_MARKETING', or 'CONTENT_NOTIFICATION'.
        :type message_content_type: Optional[MessageContentType]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: SendMessageResponse
        :rtype: SendMessageResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        recipient_dict = build_recipient_dict(
            contact_id=contact_id, recipient_identities=recipient_identities
        )
        recipient = coerce_recipient(recipient_dict)
        # Coerce message to SendMessageRequestBody if it's a dict
        if isinstance(message, dict):
            message = SendMessageRequestBody(**message)
        message_kwargs, request_kwargs = split_send_kwargs(kwargs)
        # message kwargs are applied directly to the message model (if provided as dict)
        if message_kwargs:
            message = SendMessageRequestBody(
                **message.model_dump(), **message_kwargs
            )
        request_data = SendMessageRequest(
            app_id=app_id,
            recipient=recipient,
            message=message,
            ttl=ttl,
            callback_url=callback_url,
            channel_priority_order=channel_priority_order,
            channel_properties=channel_properties,
            message_metadata=message_metadata,
            conversation_metadata=conversation_metadata,
            queue=queue,
            processing_strategy=processing_strategy,
            correlation_id=correlation_id,
            conversation_metadata_update_strategy=conversation_metadata_update_strategy,
            message_content_type=message_content_type,
            **request_kwargs,
        )
        return self._request(SendMessageEndpoint, request_data)

    def send_text_message(
        self,
        app_id: str,
        text: str,
        contact_id: Optional[str] = None,
        recipient_identities: Optional[
            List[ChannelRecipientIdentityDict]
        ] = None,
        ttl: Optional[Union[str, int]] = None,
        callback_url: Optional[str] = None,
        channel_priority_order: Optional[List[ConversationChannelType]] = None,
        channel_properties: Optional[Dict[str, str]] = None,
        message_metadata: Optional[str] = None,
        conversation_metadata: Optional[Dict[str, Any]] = None,
        queue: Optional[MessageQueueType] = None,
        processing_strategy: Optional[ProcessingStrategyType] = None,
        correlation_id: Optional[str] = None,
        conversation_metadata_update_strategy: Optional[
            MetadataUpdateStrategyType
        ] = None,
        message_content_type: Optional[MessageContentType] = None,
        **kwargs,
    ) -> SendMessageResponse:
        """
        Send a text message from a Conversation app to a contact associated with that app.
        If the recipient is not associated with an existing contact, a new contact will be created.
        The message is added to the active conversation with the contact if a conversation already exists.
        If no active conversation exists a new one is started automatically.

        :param app_id: The ID of the Conversation API app sending the message.
        :type app_id: str
        :param contact_id: The contact ID of the recipient. Either contact_id or recipient_identities must be provided.
        :type contact_id: Optional[str]
        :param recipient_identities: List of channel identities for the recipient. Either contact_id or recipient_identities must be provided.
        :type recipient_identities: Optional[List[ChannelRecipientIdentityDict]]
        :param text: The text content of the message.
        :type text: str
        :param ttl: The timeout allotted for sending the message. Can be seconds (int) or a string like '10s'.
        :type ttl: Optional[Union[str, int]]
        :param callback_url: Overwrites the default callback url for delivery receipts for this message.
        :type callback_url: Optional[str]
        :param channel_priority_order: Explicitly define the channels and order in which they are tried when sending the message.
        :type channel_priority_order: Optional[List[ConversationChannelType]]
        :param channel_properties: Channel-specific properties. The key in the map must point to a valid channel property key.
        :type channel_properties: Optional[Dict[str, str]]
        :param message_metadata: Metadata that should be associated with the message. Up to 1024 characters long.
        :type message_metadata: Optional[str]
        :param conversation_metadata: Metadata that will be associated with the conversation. Up to 2048 characters long.
        :type conversation_metadata: Optional[Dict[str, Any]]
        :param queue: Select the priority type for the message. Can be 'NORMAL_PRIORITY' or 'HIGH_PRIORITY'.
        :type queue: Optional[MessageQueueType]
        :param processing_strategy: Overrides the app's Processing Mode. Can be 'DEFAULT' or 'DISPATCH_ONLY'.
        :type processing_strategy: Optional[ProcessingStrategyType]
        :param correlation_id: An arbitrary identifier that will be propagated to callbacks related to this message. Up to 128 characters long.
        :type correlation_id: Optional[str]
        :param conversation_metadata_update_strategy: Update strategy for the conversation_metadata field. Can be 'REPLACE' or 'MERGE_PATCH'.
        :type conversation_metadata_update_strategy: Optional[MetadataUpdateStrategyType]
        :param message_content_type: Classifies the message content for use with consent management. Can be 'CONTENT_UNKNOWN', 'CONTENT_MARKETING', or 'CONTENT_NOTIFICATION'.
        :type message_content_type: Optional[MessageContentType]
        :param **kwargs: Additional parameters for the message body (e.g., agent, etc.).
        :type **kwargs: dict

        :returns: SendMessageResponse
        :rtype: SendMessageResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        return self._send_message_variant(
            app_id=app_id,
            contact_id=contact_id,
            recipient_identities=recipient_identities,
            message_field="text_message",
            message=TextMessage(text=text),
            message_cls=TextMessage,
            ttl=ttl,
            callback_url=callback_url,
            channel_priority_order=channel_priority_order,
            channel_properties=channel_properties,
            message_metadata=message_metadata,
            conversation_metadata=conversation_metadata,
            queue=queue,
            processing_strategy=processing_strategy,
            correlation_id=correlation_id,
            conversation_metadata_update_strategy=conversation_metadata_update_strategy,
            message_content_type=message_content_type,
            **kwargs,
        )

    def send_card_message(
        self,
        app_id: str,
        card_message: CardMessageDict,
        contact_id: Optional[str] = None,
        recipient_identities: Optional[
            List[ChannelRecipientIdentityDict]
        ] = None,
        ttl: Optional[Union[str, int]] = None,
        callback_url: Optional[str] = None,
        channel_priority_order: Optional[List[ConversationChannelType]] = None,
        channel_properties: Optional[Dict[str, str]] = None,
        message_metadata: Optional[str] = None,
        conversation_metadata: Optional[Dict[str, Any]] = None,
        queue: Optional[MessageQueueType] = None,
        processing_strategy: Optional[ProcessingStrategyType] = None,
        correlation_id: Optional[str] = None,
        conversation_metadata_update_strategy: Optional[
            MetadataUpdateStrategyType
        ] = None,
        message_content_type: Optional[MessageContentType] = None,
        **kwargs,
    ) -> SendMessageResponse:
        """
        Send a card message from a Conversation app to a contact associated with that app.
        If the recipient is not associated with an existing contact, a new contact will be created.
        The message is added to the active conversation with the contact if a conversation already exists.
        If no active conversation exists a new one is started automatically.

        :param app_id: The ID of the Conversation API app sending the message.
        :type app_id: str
        :param contact_id: The contact ID of the recipient. Either contact_id or recipient_identities must be provided.
        :type contact_id: Optional[str]
        :param recipient_identities: List of channel identities for the recipient. Either contact_id or recipient_identities must be provided.
        :type recipient_identities: Optional[List[ChannelRecipientIdentityDict]]
        :param card_message: The card message content.
        :type card_message: CardMessageDict
        :param ttl: The timeout allotted for sending the message. Can be seconds (int) or a string like '10s'.
        :type ttl: Optional[Union[str, int]]
        :param callback_url: Overwrites the default callback url for delivery receipts for this message.
        :type callback_url: Optional[str]
        :param channel_priority_order: Explicitly define the channels and order in which they are tried when sending the message.
        :type channel_priority_order: Optional[List[ConversationChannelType]]
        :param channel_properties: Channel-specific properties. The key in the map must point to a valid channel property key.
        :type channel_properties: Optional[Dict[str, str]]
        :param message_metadata: Metadata that should be associated with the message. Up to 1024 characters long.
        :type message_metadata: Optional[str]
        :param conversation_metadata: Metadata that will be associated with the conversation. Up to 2048 characters long.
        :type conversation_metadata: Optional[Dict[str, Any]]
        :param queue: Select the priority type for the message. Can be 'NORMAL_PRIORITY' or 'HIGH_PRIORITY'.
        :type queue: Optional[MessageQueueType]
        :param processing_strategy: Overrides the app's Processing Mode. Can be 'DEFAULT' or 'DISPATCH_ONLY'.
        :type processing_strategy: Optional[ProcessingStrategyType]
        :param correlation_id: An arbitrary identifier that will be propagated to callbacks related to this message. Up to 128 characters long.
        :type correlation_id: Optional[str]
        :param conversation_metadata_update_strategy: Update strategy for the conversation_metadata field. Can be 'REPLACE' or 'MERGE_PATCH'.
        :type conversation_metadata_update_strategy: Optional[MetadataUpdateStrategyType]
        :param message_content_type: Classifies the message content for use with consent management. Can be 'CONTENT_UNKNOWN', 'CONTENT_MARKETING', or 'CONTENT_NOTIFICATION'.
        :type message_content_type: Optional[MessageContentType]
        :param **kwargs: Additional parameters for the message body (e.g., agent, etc.).
        :type **kwargs: dict

        :returns: SendMessageResponse
        :rtype: SendMessageResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        return self._send_message_variant(
            app_id=app_id,
            contact_id=contact_id,
            recipient_identities=recipient_identities,
            message_field="card_message",
            message=card_message,
            message_cls=CardMessage,
            ttl=ttl,
            callback_url=callback_url,
            channel_priority_order=channel_priority_order,
            channel_properties=channel_properties,
            message_metadata=message_metadata,
            conversation_metadata=conversation_metadata,
            queue=queue,
            processing_strategy=processing_strategy,
            correlation_id=correlation_id,
            conversation_metadata_update_strategy=conversation_metadata_update_strategy,
            message_content_type=message_content_type,
            **kwargs,
        )

    def send_carousel_message(
        self,
        app_id: str,
        carousel_message: CarouselMessageDict,
        contact_id: Optional[str] = None,
        recipient_identities: Optional[
            List[ChannelRecipientIdentityDict]
        ] = None,
        ttl: Optional[Union[str, int]] = None,
        callback_url: Optional[str] = None,
        channel_priority_order: Optional[List[ConversationChannelType]] = None,
        channel_properties: Optional[Dict[str, str]] = None,
        message_metadata: Optional[str] = None,
        conversation_metadata: Optional[Dict[str, Any]] = None,
        queue: Optional[MessageQueueType] = None,
        processing_strategy: Optional[ProcessingStrategyType] = None,
        correlation_id: Optional[str] = None,
        conversation_metadata_update_strategy: Optional[
            MetadataUpdateStrategyType
        ] = None,
        message_content_type: Optional[MessageContentType] = None,
        **kwargs,
    ) -> SendMessageResponse:
        """
        Send a carousel message from a Conversation app to a contact associated with that app.
        If the recipient is not associated with an existing contact, a new contact will be created.
        The message is added to the active conversation with the contact if a conversation already exists.
        If no active conversation exists a new one is started automatically.

        :param app_id: The ID of the Conversation API app sending the message.
        :type app_id: str
        :param contact_id: The contact ID of the recipient. Either contact_id or recipient_identities must be provided.
        :type contact_id: Optional[str]
        :param recipient_identities: List of channel identities for the recipient. Either contact_id or recipient_identities must be provided.
        :type recipient_identities: Optional[List[ChannelRecipientIdentityDict]]
        :param carousel_message: The carousel message content.
        :type carousel_message: CarouselMessageDict
        :param ttl: The timeout allotted for sending the message. Can be seconds (int) or a string like '10s'.
        :type ttl: Optional[Union[str, int]]
        :param callback_url: Overwrites the default callback url for delivery receipts for this message.
        :type callback_url: Optional[str]
        :param channel_priority_order: Explicitly define the channels and order in which they are tried when sending the message.
        :type channel_priority_order: Optional[List[ConversationChannelType]]
        :param channel_properties: Channel-specific properties. The key in the map must point to a valid channel property key.
        :type channel_properties: Optional[Dict[str, str]]
        :param message_metadata: Metadata that should be associated with the message. Up to 1024 characters long.
        :type message_metadata: Optional[str]
        :param conversation_metadata: Metadata that will be associated with the conversation. Up to 2048 characters long.
        :type conversation_metadata: Optional[Dict[str, Any]]
        :param queue: Select the priority type for the message. Can be 'NORMAL_PRIORITY' or 'HIGH_PRIORITY'.
        :type queue: Optional[MessageQueueType]
        :param processing_strategy: Overrides the app's Processing Mode. Can be 'DEFAULT' or 'DISPATCH_ONLY'.
        :type processing_strategy: Optional[ProcessingStrategyType]
        :param correlation_id: An arbitrary identifier that will be propagated to callbacks related to this message. Up to 128 characters long.
        :type correlation_id: Optional[str]
        :param conversation_metadata_update_strategy: Update strategy for the conversation_metadata field. Can be 'REPLACE' or 'MERGE_PATCH'.
        :type conversation_metadata_update_strategy: Optional[MetadataUpdateStrategyType]
        :param message_content_type: Classifies the message content for use with consent management. Can be 'CONTENT_UNKNOWN', 'CONTENT_MARKETING', or 'CONTENT_NOTIFICATION'.
        :type message_content_type: Optional[MessageContentType]
        :param **kwargs: Additional parameters for the message body (e.g., agent, etc.).
        :type **kwargs: dict

        :returns: SendMessageResponse
        :rtype: SendMessageResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        return self._send_message_variant(
            app_id=app_id,
            contact_id=contact_id,
            recipient_identities=recipient_identities,
            message_field="carousel_message",
            message=carousel_message,
            message_cls=CarouselMessage,
            ttl=ttl,
            callback_url=callback_url,
            channel_priority_order=channel_priority_order,
            channel_properties=channel_properties,
            message_metadata=message_metadata,
            conversation_metadata=conversation_metadata,
            queue=queue,
            processing_strategy=processing_strategy,
            correlation_id=correlation_id,
            conversation_metadata_update_strategy=conversation_metadata_update_strategy,
            message_content_type=message_content_type,
            **kwargs,
        )

    def send_choice_message(
        self,
        app_id: str,
        choice_message: ChoiceMessageDict,
        contact_id: Optional[str] = None,
        recipient_identities: Optional[
            List[ChannelRecipientIdentityDict]
        ] = None,
        ttl: Optional[Union[str, int]] = None,
        callback_url: Optional[str] = None,
        channel_priority_order: Optional[List[ConversationChannelType]] = None,
        channel_properties: Optional[Dict[str, str]] = None,
        message_metadata: Optional[str] = None,
        conversation_metadata: Optional[Dict[str, Any]] = None,
        queue: Optional[MessageQueueType] = None,
        processing_strategy: Optional[ProcessingStrategyType] = None,
        correlation_id: Optional[str] = None,
        conversation_metadata_update_strategy: Optional[
            MetadataUpdateStrategyType
        ] = None,
        message_content_type: Optional[MessageContentType] = None,
        **kwargs,
    ) -> SendMessageResponse:
        """
        Send a choice message from a Conversation app to a contact associated with that app.
        If the recipient is not associated with an existing contact, a new contact will be created.
        The message is added to the active conversation with the contact if a conversation already exists.
        If no active conversation exists a new one is started automatically.

        :param app_id: The ID of the Conversation API app sending the message.
        :type app_id: str
        :param contact_id: The contact ID of the recipient. Either contact_id or recipient_identities must be provided.
        :type contact_id: Optional[str]
        :param recipient_identities: List of channel identities for the recipient. Either contact_id or recipient_identities must be provided.
        :type recipient_identities: Optional[List[ChannelRecipientIdentityDict]]
        :param choice_message: The choice message content.
        :type choice_message: ChoiceMessageDict
        :param ttl: The timeout allotted for sending the message. Can be seconds (int) or a string like '10s'.
        :type ttl: Optional[Union[str, int]]
        :param callback_url: Overwrites the default callback url for delivery receipts for this message.
        :type callback_url: Optional[str]
        :param channel_priority_order: Explicitly define the channels and order in which they are tried when sending the message.
        :type channel_priority_order: Optional[List[ConversationChannelType]]
        :param channel_properties: Channel-specific properties. The key in the map must point to a valid channel property key.
        :type channel_properties: Optional[Dict[str, str]]
        :param message_metadata: Metadata that should be associated with the message. Up to 1024 characters long.
        :type message_metadata: Optional[str]
        :param conversation_metadata: Metadata that will be associated with the conversation. Up to 2048 characters long.
        :type conversation_metadata: Optional[Dict[str, Any]]
        :param queue: Select the priority type for the message. Can be 'NORMAL_PRIORITY' or 'HIGH_PRIORITY'.
        :type queue: Optional[MessageQueueType]
        :param processing_strategy: Overrides the app's Processing Mode. Can be 'DEFAULT' or 'DISPATCH_ONLY'.
        :type processing_strategy: Optional[ProcessingStrategyType]
        :param correlation_id: An arbitrary identifier that will be propagated to callbacks related to this message. Up to 128 characters long.
        :type correlation_id: Optional[str]
        :param conversation_metadata_update_strategy: Update strategy for the conversation_metadata field. Can be 'REPLACE' or 'MERGE_PATCH'.
        :type conversation_metadata_update_strategy: Optional[MetadataUpdateStrategyType]
        :param message_content_type: Classifies the message content for use with consent management. Can be 'CONTENT_UNKNOWN', 'CONTENT_MARKETING', or 'CONTENT_NOTIFICATION'.
        :type message_content_type: Optional[MessageContentType]
        :param **kwargs: Additional parameters for the message body (e.g., agent, etc.).
        :type **kwargs: dict

        :returns: SendMessageResponse
        :rtype: SendMessageResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        return self._send_message_variant(
            app_id=app_id,
            contact_id=contact_id,
            recipient_identities=recipient_identities,
            message_field="choice_message",
            message=choice_message,
            message_cls=ChoiceMessage,
            ttl=ttl,
            callback_url=callback_url,
            channel_priority_order=channel_priority_order,
            channel_properties=channel_properties,
            message_metadata=message_metadata,
            conversation_metadata=conversation_metadata,
            queue=queue,
            processing_strategy=processing_strategy,
            correlation_id=correlation_id,
            conversation_metadata_update_strategy=conversation_metadata_update_strategy,
            message_content_type=message_content_type,
            **kwargs,
        )

    def send_contact_info_message(
        self,
        app_id: str,
        contact_info_message: ContactInfoMessageDict,
        contact_id: Optional[str] = None,
        recipient_identities: Optional[
            List[ChannelRecipientIdentityDict]
        ] = None,
        ttl: Optional[Union[str, int]] = None,
        callback_url: Optional[str] = None,
        channel_priority_order: Optional[List[ConversationChannelType]] = None,
        channel_properties: Optional[Dict[str, str]] = None,
        message_metadata: Optional[str] = None,
        conversation_metadata: Optional[Dict[str, Any]] = None,
        queue: Optional[MessageQueueType] = None,
        processing_strategy: Optional[ProcessingStrategyType] = None,
        correlation_id: Optional[str] = None,
        conversation_metadata_update_strategy: Optional[
            MetadataUpdateStrategyType
        ] = None,
        message_content_type: Optional[MessageContentType] = None,
        **kwargs,
    ) -> SendMessageResponse:
        """
        Send a contact info message from a Conversation app to a contact associated with that app.
        If the recipient is not associated with an existing contact, a new contact will be created.
        The message is added to the active conversation with the contact if a conversation already exists.
        If no active conversation exists a new one is started automatically.

        :param app_id: The ID of the Conversation API app sending the message.
        :type app_id: str
        :param contact_id: The contact ID of the recipient. Either contact_id or recipient_identities must be provided.
        :type contact_id: Optional[str]
        :param recipient_identities: List of channel identities for the recipient. Either contact_id or recipient_identities must be provided.
        :type recipient_identities: Optional[List[ChannelRecipientIdentityDict]]
        :param contact_info_message: The contact info message content.
        :type contact_info_message: ContactInfoMessageDict
        :param ttl: The timeout allotted for sending the message. Can be seconds (int) or a string like '10s'.
        :type ttl: Optional[Union[str, int]]
        :param callback_url: Overwrites the default callback url for delivery receipts for this message.
        :type callback_url: Optional[str]
        :param channel_priority_order: Explicitly define the channels and order in which they are tried when sending the message.
        :type channel_priority_order: Optional[List[ConversationChannelType]]
        :param channel_properties: Channel-specific properties. The key in the map must point to a valid channel property key.
        :type channel_properties: Optional[Dict[str, str]]
        :param message_metadata: Metadata that should be associated with the message. Up to 1024 characters long.
        :type message_metadata: Optional[str]
        :param conversation_metadata: Metadata that will be associated with the conversation. Up to 2048 characters long.
        :type conversation_metadata: Optional[Dict[str, Any]]
        :param queue: Select the priority type for the message. Can be 'NORMAL_PRIORITY' or 'HIGH_PRIORITY'.
        :type queue: Optional[MessageQueueType]
        :param processing_strategy: Overrides the app's Processing Mode. Can be 'DEFAULT' or 'DISPATCH_ONLY'.
        :type processing_strategy: Optional[ProcessingStrategyType]
        :param correlation_id: An arbitrary identifier that will be propagated to callbacks related to this message. Up to 128 characters long.
        :type correlation_id: Optional[str]
        :param conversation_metadata_update_strategy: Update strategy for the conversation_metadata field. Can be 'REPLACE' or 'MERGE_PATCH'.
        :type conversation_metadata_update_strategy: Optional[MetadataUpdateStrategyType]
        :param message_content_type: Classifies the message content for use with consent management. Can be 'CONTENT_UNKNOWN', 'CONTENT_MARKETING', or 'CONTENT_NOTIFICATION'.
        :type message_content_type: Optional[MessageContentType]
        :param **kwargs: Additional parameters for the message body (e.g., agent, etc.).
        :type **kwargs: dict

        :returns: SendMessageResponse
        :rtype: SendMessageResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        return self._send_message_variant(
            app_id=app_id,
            contact_id=contact_id,
            recipient_identities=recipient_identities,
            message_field="contact_info_message",
            message=contact_info_message,
            message_cls=ContactInfoMessage,
            ttl=ttl,
            callback_url=callback_url,
            channel_priority_order=channel_priority_order,
            channel_properties=channel_properties,
            message_metadata=message_metadata,
            conversation_metadata=conversation_metadata,
            queue=queue,
            processing_strategy=processing_strategy,
            correlation_id=correlation_id,
            conversation_metadata_update_strategy=conversation_metadata_update_strategy,
            message_content_type=message_content_type,
            **kwargs,
        )

    def send_list_message(
        self,
        app_id: str,
        list_message: ListMessageDict,
        contact_id: Optional[str] = None,
        recipient_identities: Optional[
            List[ChannelRecipientIdentityDict]
        ] = None,
        ttl: Optional[Union[str, int]] = None,
        callback_url: Optional[str] = None,
        channel_priority_order: Optional[List[ConversationChannelType]] = None,
        channel_properties: Optional[Dict[str, str]] = None,
        message_metadata: Optional[str] = None,
        conversation_metadata: Optional[Dict[str, Any]] = None,
        queue: Optional[MessageQueueType] = None,
        processing_strategy: Optional[ProcessingStrategyType] = None,
        correlation_id: Optional[str] = None,
        conversation_metadata_update_strategy: Optional[
            MetadataUpdateStrategyType
        ] = None,
        message_content_type: Optional[MessageContentType] = None,
        **kwargs,
    ) -> SendMessageResponse:
        """
        Send a list message from a Conversation app to a contact associated with that app.
        If the recipient is not associated with an existing contact, a new contact will be created.
        The message is added to the active conversation with the contact if a conversation already exists.
        If no active conversation exists a new one is started automatically.

        :param app_id: The ID of the Conversation API app sending the message.
        :type app_id: str
        :param contact_id: The contact ID of the recipient. Either contact_id or recipient_identities must be provided.
        :type contact_id: Optional[str]
        :param recipient_identities: List of channel identities for the recipient. Either contact_id or recipient_identities must be provided.
        :type recipient_identities: Optional[List[ChannelRecipientIdentityDict]]
        :param list_message: The list message content.
        :type list_message: ListMessageDict
        :param ttl: The timeout allotted for sending the message. Can be seconds (int) or a string like '10s'.
        :type ttl: Optional[Union[str, int]]
        :param callback_url: Overwrites the default callback url for delivery receipts for this message.
        :type callback_url: Optional[str]
        :param channel_priority_order: Explicitly define the channels and order in which they are tried when sending the message.
        :type channel_priority_order: Optional[List[ConversationChannelType]]
        :param channel_properties: Channel-specific properties. The key in the map must point to a valid channel property key.
        :type channel_properties: Optional[Dict[str, str]]
        :param message_metadata: Metadata that should be associated with the message. Up to 1024 characters long.
        :type message_metadata: Optional[str]
        :param conversation_metadata: Metadata that will be associated with the conversation. Up to 2048 characters long.
        :type conversation_metadata: Optional[Dict[str, Any]]
        :param queue: Select the priority type for the message. Can be 'NORMAL_PRIORITY' or 'HIGH_PRIORITY'.
        :type queue: Optional[MessageQueueType]
        :param processing_strategy: Overrides the app's Processing Mode. Can be 'DEFAULT' or 'DISPATCH_ONLY'.
        :type processing_strategy: Optional[ProcessingStrategyType]
        :param correlation_id: An arbitrary identifier that will be propagated to callbacks related to this message. Up to 128 characters long.
        :type correlation_id: Optional[str]
        :param conversation_metadata_update_strategy: Update strategy for the conversation_metadata field. Can be 'REPLACE' or 'MERGE_PATCH'.
        :type conversation_metadata_update_strategy: Optional[MetadataUpdateStrategyType]
        :param message_content_type: Classifies the message content for use with consent management. Can be 'CONTENT_UNKNOWN', 'CONTENT_MARKETING', or 'CONTENT_NOTIFICATION'.
        :type message_content_type: Optional[MessageContentType]
        :param **kwargs: Additional parameters for the message body (e.g., agent, etc.).
        :type **kwargs: dict

        :returns: SendMessageResponse
        :rtype: SendMessageResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        return self._send_message_variant(
            app_id=app_id,
            contact_id=contact_id,
            recipient_identities=recipient_identities,
            message_field="list_message",
            message=list_message,
            message_cls=ListMessage,
            ttl=ttl,
            callback_url=callback_url,
            channel_priority_order=channel_priority_order,
            channel_properties=channel_properties,
            message_metadata=message_metadata,
            conversation_metadata=conversation_metadata,
            queue=queue,
            processing_strategy=processing_strategy,
            correlation_id=correlation_id,
            conversation_metadata_update_strategy=conversation_metadata_update_strategy,
            message_content_type=message_content_type,
            **kwargs,
        )

    def send_location_message(
        self,
        app_id: str,
        location_message: LocationMessageDict,
        contact_id: Optional[str] = None,
        recipient_identities: Optional[
            List[ChannelRecipientIdentityDict]
        ] = None,
        ttl: Optional[Union[str, int]] = None,
        callback_url: Optional[str] = None,
        channel_priority_order: Optional[List[ConversationChannelType]] = None,
        channel_properties: Optional[Dict[str, str]] = None,
        message_metadata: Optional[str] = None,
        conversation_metadata: Optional[Dict[str, Any]] = None,
        queue: Optional[MessageQueueType] = None,
        processing_strategy: Optional[ProcessingStrategyType] = None,
        correlation_id: Optional[str] = None,
        conversation_metadata_update_strategy: Optional[
            MetadataUpdateStrategyType
        ] = None,
        message_content_type: Optional[MessageContentType] = None,
        **kwargs,
    ) -> SendMessageResponse:
        """
        Send a location message from a Conversation app to a contact associated with that app.
        If the recipient is not associated with an existing contact, a new contact will be created.
        The message is added to the active conversation with the contact if a conversation already exists.
        If no active conversation exists a new one is started automatically.

        :param app_id: The ID of the Conversation API app sending the message.
        :type app_id: str
        :param contact_id: The contact ID of the recipient. Either contact_id or recipient_identities must be provided.
        :type contact_id: Optional[str]
        :param recipient_identities: List of channel identities for the recipient. Either contact_id or recipient_identities must be provided.
        :type recipient_identities: Optional[List[ChannelRecipientIdentityDict]]
        :param location_message: The location message content.
        :type location_message: LocationMessageDict
        :param ttl: The timeout allotted for sending the message. Can be seconds (int) or a string like '10s'.
        :type ttl: Optional[Union[str, int]]
        :param callback_url: Overwrites the default callback url for delivery receipts for this message.
        :type callback_url: Optional[str]
        :param channel_priority_order: Explicitly define the channels and order in which they are tried when sending the message.
        :type channel_priority_order: Optional[List[ConversationChannelType]]
        :param channel_properties: Channel-specific properties. The key in the map must point to a valid channel property key.
        :type channel_properties: Optional[Dict[str, str]]
        :param message_metadata: Metadata that should be associated with the message. Up to 1024 characters long.
        :type message_metadata: Optional[str]
        :param conversation_metadata: Metadata that will be associated with the conversation. Up to 2048 characters long.
        :type conversation_metadata: Optional[Dict[str, Any]]
        :param queue: Select the priority type for the message. Can be 'NORMAL_PRIORITY' or 'HIGH_PRIORITY'.
        :type queue: Optional[MessageQueueType]
        :param processing_strategy: Overrides the app's Processing Mode. Can be 'DEFAULT' or 'DISPATCH_ONLY'.
        :type processing_strategy: Optional[ProcessingStrategyType]
        :param correlation_id: An arbitrary identifier that will be propagated to callbacks related to this message. Up to 128 characters long.
        :type correlation_id: Optional[str]
        :param conversation_metadata_update_strategy: Update strategy for the conversation_metadata field. Can be 'REPLACE' or 'MERGE_PATCH'.
        :type conversation_metadata_update_strategy: Optional[MetadataUpdateStrategyType]
        :param message_content_type: Classifies the message content for use with consent management. Can be 'CONTENT_UNKNOWN', 'CONTENT_MARKETING', or 'CONTENT_NOTIFICATION'.
        :type message_content_type: Optional[MessageContentType]
        :param **kwargs: Additional parameters for the message body (e.g., agent, etc.).
        :type **kwargs: dict

        :returns: SendMessageResponse
        :rtype: SendMessageResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        return self._send_message_variant(
            app_id=app_id,
            contact_id=contact_id,
            recipient_identities=recipient_identities,
            message_field="location_message",
            message=location_message,
            message_cls=LocationMessage,
            ttl=ttl,
            callback_url=callback_url,
            channel_priority_order=channel_priority_order,
            channel_properties=channel_properties,
            message_metadata=message_metadata,
            conversation_metadata=conversation_metadata,
            queue=queue,
            processing_strategy=processing_strategy,
            correlation_id=correlation_id,
            conversation_metadata_update_strategy=conversation_metadata_update_strategy,
            message_content_type=message_content_type,
            **kwargs,
        )

    def send_media_message(
        self,
        app_id: str,
        media_message: MediaPropertiesDict,
        contact_id: Optional[str] = None,
        recipient_identities: Optional[
            List[ChannelRecipientIdentityDict]
        ] = None,
        ttl: Optional[Union[str, int]] = None,
        callback_url: Optional[str] = None,
        channel_priority_order: Optional[List[ConversationChannelType]] = None,
        channel_properties: Optional[Dict[str, str]] = None,
        message_metadata: Optional[str] = None,
        conversation_metadata: Optional[Dict[str, Any]] = None,
        queue: Optional[MessageQueueType] = None,
        processing_strategy: Optional[ProcessingStrategyType] = None,
        correlation_id: Optional[str] = None,
        conversation_metadata_update_strategy: Optional[
            MetadataUpdateStrategyType
        ] = None,
        message_content_type: Optional[MessageContentType] = None,
        **kwargs,
    ) -> SendMessageResponse:
        """
        Send a media message from a Conversation app to a contact associated with that app.
        If the recipient is not associated with an existing contact, a new contact will be created.
        The message is added to the active conversation with the contact if a conversation already exists.
        If no active conversation exists a new one is started automatically.

        :param app_id: The ID of the Conversation API app sending the message.
        :type app_id: str
        :param contact_id: The contact ID of the recipient. Either contact_id or recipient_identities must be provided.
        :type contact_id: Optional[str]
        :param recipient_identities: List of channel identities for the recipient. Either contact_id or recipient_identities must be provided.
        :type recipient_identities: Optional[List[ChannelRecipientIdentityDict]]
        :param media_message: The media message content.
        :type media_message: MediaPropertiesDict
        :param ttl: The timeout allotted for sending the message. Can be seconds (int) or a string like '10s'.
        :type ttl: Optional[Union[str, int]]
        :param callback_url: Overwrites the default callback url for delivery receipts for this message.
        :type callback_url: Optional[str]
        :param channel_priority_order: Explicitly define the channels and order in which they are tried when sending the message.
        :type channel_priority_order: Optional[List[ConversationChannelType]]
        :param channel_properties: Channel-specific properties. The key in the map must point to a valid channel property key.
        :type channel_properties: Optional[Dict[str, str]]
        :param message_metadata: Metadata that should be associated with the message. Up to 1024 characters long.
        :type message_metadata: Optional[str]
        :param conversation_metadata: Metadata that will be associated with the conversation. Up to 2048 characters long.
        :type conversation_metadata: Optional[Dict[str, Any]]
        :param queue: Select the priority type for the message. Can be 'NORMAL_PRIORITY' or 'HIGH_PRIORITY'.
        :type queue: Optional[MessageQueueType]
        :param processing_strategy: Overrides the app's Processing Mode. Can be 'DEFAULT' or 'DISPATCH_ONLY'.
        :type processing_strategy: Optional[ProcessingStrategyType]
        :param correlation_id: An arbitrary identifier that will be propagated to callbacks related to this message. Up to 128 characters long.
        :type correlation_id: Optional[str]
        :param conversation_metadata_update_strategy: Update strategy for the conversation_metadata field. Can be 'REPLACE' or 'MERGE_PATCH'.
        :type conversation_metadata_update_strategy: Optional[MetadataUpdateStrategyType]
        :param message_content_type: Classifies the message content for use with consent management. Can be 'CONTENT_UNKNOWN', 'CONTENT_MARKETING', or 'CONTENT_NOTIFICATION'.
        :type message_content_type: Optional[MessageContentType]
        :param **kwargs: Additional parameters for the message body (e.g., agent, etc.).
        :type **kwargs: dict

        :returns: SendMessageResponse
        :rtype: SendMessageResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        return self._send_message_variant(
            app_id=app_id,
            contact_id=contact_id,
            recipient_identities=recipient_identities,
            message_field="media_message",
            message=media_message,
            message_cls=MediaProperties,
            ttl=ttl,
            callback_url=callback_url,
            channel_priority_order=channel_priority_order,
            channel_properties=channel_properties,
            message_metadata=message_metadata,
            conversation_metadata=conversation_metadata,
            queue=queue,
            processing_strategy=processing_strategy,
            correlation_id=correlation_id,
            conversation_metadata_update_strategy=conversation_metadata_update_strategy,
            message_content_type=message_content_type,
            **kwargs,
        )

    def send_template_message(
        self,
        app_id: str,
        template_message: TemplateMessageDict,
        contact_id: Optional[str] = None,
        recipient_identities: Optional[
            List[ChannelRecipientIdentityDict]
        ] = None,
        ttl: Optional[Union[str, int]] = None,
        callback_url: Optional[str] = None,
        channel_priority_order: Optional[List[ConversationChannelType]] = None,
        channel_properties: Optional[Dict[str, str]] = None,
        message_metadata: Optional[str] = None,
        conversation_metadata: Optional[Dict[str, Any]] = None,
        queue: Optional[MessageQueueType] = None,
        processing_strategy: Optional[ProcessingStrategyType] = None,
        correlation_id: Optional[str] = None,
        conversation_metadata_update_strategy: Optional[
            MetadataUpdateStrategyType
        ] = None,
        message_content_type: Optional[MessageContentType] = None,
        **kwargs,
    ) -> SendMessageResponse:
        """
        Send a template message from a Conversation app to a contact associated with that app.
        If the recipient is not associated with an existing contact, a new contact will be created.
        The message is added to the active conversation with the contact if a conversation already exists.
        If no active conversation exists a new one is started automatically.

        :param app_id: The ID of the Conversation API app sending the message.
        :type app_id: str
        :param contact_id: The contact ID of the recipient. Either contact_id or recipient_identities must be provided.
        :type contact_id: Optional[str]
        :param recipient_identities: List of channel identities for the recipient. Either contact_id or recipient_identities must be provided.
        :type recipient_identities: Optional[List[ChannelRecipientIdentityDict]]
        :param template_message: The template message content.
        :type template_message: TemplateMessageDict
        :param ttl: The timeout allotted for sending the message. Can be seconds (int) or a string like '10s'.
        :type ttl: Optional[Union[str, int]]
        :param callback_url: Overwrites the default callback url for delivery receipts for this message.
        :type callback_url: Optional[str]
        :param channel_priority_order: Explicitly define the channels and order in which they are tried when sending the message.
        :type channel_priority_order: Optional[List[ConversationChannelType]]
        :param channel_properties: Channel-specific properties. The key in the map must point to a valid channel property key.
        :type channel_properties: Optional[Dict[str, str]]
        :param message_metadata: Metadata that should be associated with the message. Up to 1024 characters long.
        :type message_metadata: Optional[str]
        :param conversation_metadata: Metadata that will be associated with the conversation. Up to 2048 characters long.
        :type conversation_metadata: Optional[Dict[str, Any]]
        :param queue: Select the priority type for the message. Can be 'NORMAL_PRIORITY' or 'HIGH_PRIORITY'.
        :type queue: Optional[MessageQueueType]
        :param processing_strategy: Overrides the app's Processing Mode. Can be 'DEFAULT' or 'DISPATCH_ONLY'.
        :type processing_strategy: Optional[ProcessingStrategyType]
        :param correlation_id: An arbitrary identifier that will be propagated to callbacks related to this message. Up to 128 characters long.
        :type correlation_id: Optional[str]
        :param conversation_metadata_update_strategy: Update strategy for the conversation_metadata field. Can be 'REPLACE' or 'MERGE_PATCH'.
        :type conversation_metadata_update_strategy: Optional[MetadataUpdateStrategyType]
        :param message_content_type: Classifies the message content for use with consent management. Can be 'CONTENT_UNKNOWN', 'CONTENT_MARKETING', or 'CONTENT_NOTIFICATION'.
        :type message_content_type: Optional[MessageContentType]
        :param **kwargs: Additional parameters for the message body (e.g., agent, etc.).
        :type **kwargs: dict

        :returns: SendMessageResponse
        :rtype: SendMessageResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        return self._send_message_variant(
            app_id=app_id,
            contact_id=contact_id,
            recipient_identities=recipient_identities,
            message_field="template_message",
            message=template_message,
            message_cls=TemplateMessage,
            ttl=ttl,
            callback_url=callback_url,
            channel_priority_order=channel_priority_order,
            channel_properties=channel_properties,
            message_metadata=message_metadata,
            conversation_metadata=conversation_metadata,
            queue=queue,
            processing_strategy=processing_strategy,
            correlation_id=correlation_id,
            conversation_metadata_update_strategy=conversation_metadata_update_strategy,
            message_content_type=message_content_type,
            **kwargs,
        )
