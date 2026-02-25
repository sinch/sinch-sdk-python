from datetime import datetime
from typing import Optional
from pydantic import Field, StrictInt, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.messages.types import (
    ConversationChannelType,
    ConversationDirectionType,
    ConversationMessagesViewType,
    MessagesSourceType,
)


class ListMessagesRequest(BaseModelConfiguration):
    """Request model for listing messages."""

    conversation_id: Optional[StrictStr] = Field(
        default=None,
        description="Filter messages by conversation ID.",
    )
    contact_id: Optional[StrictStr] = Field(
        default=None,
        description="Filter messages by contact ID.",
    )
    app_id: Optional[StrictStr] = Field(
        default=None,
        description="Filter messages by app ID.",
    )
    channel_identity: Optional[StrictStr] = Field(
        default=None,
        description="Channel identity of the contact.",
    )
    start_time: Optional[datetime] = Field(
        default=None,
        description="Filter messages with accept_time after this timestamp. Must be before end_time if that is specified.",
    )
    end_time: Optional[datetime] = Field(
        default=None,
        description="Filter messages with accept_time before this timestamp.",
    )
    page_size: Optional[StrictInt] = Field(
        default=None,
        description="Maximum number of messages to fetch. Defaults to 10 and the maximum is 1000.",
    )
    page_token: Optional[StrictStr] = Field(
        default=None,
        description="Next page token previously returned if any. When specifying this token, use the same values for the other parameters from the request that originated the token, otherwise the paged results may be inconsistent.",
    )
    view: Optional[ConversationMessagesViewType] = Field(
        default=None,
        description="Messages view type. WITH_METADATA or WITHOUT_METADATA.",
    )
    messages_source: Optional[MessagesSourceType] = Field(
        default=None,
        description="Specifies the message source for the request.",
    )
    only_recipient_originated: Optional[bool] = Field(
        default=None,
        description="Only fetch recipient-originated messages.",
    )
    channel: Optional[ConversationChannelType] = Field(
        default=None,
        description="Only fetch messages from the specified channel.",
    )
    direction: Optional[ConversationDirectionType] = Field(
        default=None,
        description="Optional. Only fetch messages with the specified direction. If direction is not specified, it will list both TO_APP and TO_CONTACT messages.",
    )
