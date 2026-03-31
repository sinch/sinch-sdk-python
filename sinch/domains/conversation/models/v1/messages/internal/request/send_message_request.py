from typing import Any, Dict, List, Optional, Union

from pydantic import Field, StrictInt, StrictStr, field_serializer
from sinch.domains.conversation.models.v1.messages.internal.request.recipient import (
    Recipient,
)
from sinch.domains.conversation.models.v1.messages.internal.request.send_message_request_body import (
    SendMessageRequestBody,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.messages.types.conversation_channel_type import (
    ConversationChannelType,
)
from sinch.domains.conversation.models.v1.messages.types.processing_strategy_type import (
    ProcessingStrategyType,
)
from sinch.domains.conversation.models.v1.messages.types.metadata_update_strategy_type import (
    MetadataUpdateStrategyType,
)
from sinch.domains.conversation.models.v1.messages.types.message_queue_type import (
    MessageQueueType,
)
from sinch.domains.conversation.models.v1.messages.types.message_content_type import (
    MessageContentType,
)


class SendMessageRequest(BaseModelConfiguration):
    app_id: StrictStr = Field(
        ...,
        description="The ID of the Conversation API app sending the message.",
    )
    recipient: Recipient = Field(
        ...,
        description="The recipient of the message.",
    )
    message: SendMessageRequestBody = Field(
        ...,
        description="The message content to send.",
    )
    ttl: Optional[Union[StrictStr, StrictInt]] = Field(
        default=None,
        description="The timeout allotted for sending the message. Can be seconds (int) or a string like '10s'.",
    )
    event_destination_target: Optional[StrictStr] = Field(
        default=None,
        alias="callback_url",
        description="Overwrites the default event destination target for delivery receipts for this message.",
    )
    channel_priority_order: Optional[List[ConversationChannelType]] = Field(
        default=None,
        description="Explicitly define the channels and order in which they are tried when sending the message.",
    )
    channel_properties: Optional[Dict[str, str]] = Field(
        default=None,
        description="Channel-specific properties. The key in the map must point to a valid channel property key.",
    )
    message_metadata: Optional[StrictStr] = Field(
        default=None,
        description="Metadata that should be associated with the message. Up to 1024 characters long.",
    )
    conversation_metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Metadata that will be associated with the conversation. Up to 2048 characters long.",
    )
    queue: Optional[MessageQueueType] = Field(
        default=None,
        description="Select the priority type for the message. Can be 'NORMAL_PRIORITY' or 'HIGH_PRIORITY'.",
    )
    processing_strategy: Optional[ProcessingStrategyType] = Field(
        default=None,
        description="Overrides the app's Processing Mode. Can be 'DEFAULT' or 'DISPATCH_ONLY'.",
    )
    correlation_id: Optional[StrictStr] = Field(
        default=None,
        description="An arbitrary identifier that will be propagated to callbacks related to this message. Up to 128 characters long.",
    )
    conversation_metadata_update_strategy: Optional[
        MetadataUpdateStrategyType
    ] = Field(
        default=None,
        description="Update strategy for the conversation_metadata field. Can be 'REPLACE' or 'MERGE_PATCH'.",
    )
    message_content_type: Optional[MessageContentType] = Field(
        default=None,
        description="Classifies the message content for use with consent management. Can be 'CONTENT_UNKNOWN', 'CONTENT_MARKETING', or 'CONTENT_NOTIFICATION'.",
    )

    @field_serializer("ttl")
    def serialize_ttl(
        self, value: Optional[Union[StrictStr, StrictInt]]
    ) -> Optional[str]:
        """
        Serialize ttl field to the format expected by the API (string with 's' suffix).
        Converts int to string with 's' suffix, or ensures string has 's' suffix.
        """
        if value is None:
            return None
        if isinstance(value, int):
            return f"{value}s"
        if isinstance(value, str) and not value.endswith("s"):
            return f"{value}s"
        return value
