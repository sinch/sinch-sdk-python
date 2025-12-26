from typing import Optional

from sinch.domains.conversation.models.v1.messages.internal import (
    DeleteMessageRequest,
    GetMessageRequest,
    UpdateMessageMetadataRequest,
)
from sinch.domains.conversation.models.v1.messages.types import (
    ConversationMessageResponse,
)
from sinch.domains.conversation.models.v1.messages.types import (
    MessagesSourceType,
)
from sinch.domains.conversation.api.v1.internal import (
    DeleteMessageEndpoint,
    GetMessageEndpoint,
    UpdateMessageMetadataEndpoint,
)
from sinch.domains.conversation.api.v1.base import BaseConversation


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
            operations on messages in Dispatch Mode. For more information,
            see [Processing Modes](https://developers.sinch.com/docs/conversation/processing-modes/).
            (optional)
        :type messages_source: Optional[MessagesSource]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: None
        :rtype: None

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = DeleteMessageRequest(
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
            operations on messages in Dispatch Mode. For more information,
            see [Processing Modes](https://developers.sinch.com/docs/conversation/processing-modes/).
            (optional)
        :type messages_source: Optional[MessagesSource]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: ConversationMessageResponse
        :rtype: ConversationMessageResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = GetMessageRequest(
            message_id=message_id, messages_source=messages_source, **kwargs
        )
        return self._request(GetMessageEndpoint, request_data)

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
            operations on messages in Dispatch Mode. For more information,
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
