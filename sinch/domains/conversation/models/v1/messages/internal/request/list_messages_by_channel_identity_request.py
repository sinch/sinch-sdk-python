from datetime import datetime
from typing import Optional
from pydantic import Field, StrictInt, StrictStr, conlist
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.messages.types import (
    ConversationChannelType,
    ConversationDirectionType,
    ConversationMessagesViewType,
    MessagesSourceType,
)


class ListLastMessagesByChannelIdentityRequest(BaseModelConfiguration):
    channel_identities: Optional[conlist(StrictStr)] = Field(
        default=None,
        description="Optional. Filter messages by channel_identity.",
    )
    contact_ids: Optional[conlist(StrictStr)] = Field(
        default=None,
        description="Optional. Resource name (id) of the contact. In CONVERSATION_SOURCE: Can list last messages by contact_id. In DISPATCH_SOURCE: The field is unsupported and cannot be set.",
    )
    app_id: Optional[StrictStr] = Field(
        default=None,
        description="Optional. Resource name (id) of the app.",
    )
    messages_source: Optional[MessagesSourceType] = Field(
        default=None,
        description="Specifies the message source for the request.",
    )
    page_size: Optional[StrictInt] = Field(
        default=None,
        description="Optional. Maximum number of messages to fetch. Defaults to 10 and the maximum is 1000.",
    )
    page_token: Optional[StrictStr] = Field(
        default=None,
        description="Optional. Next page token previously returned if any.",
    )
    view: Optional[ConversationMessagesViewType] = Field(
        default=None,
        description="Optional. Specifies the representation in which messages should be returned. Defaults to WITH_METADATA.",
    )
    start_time: Optional[datetime] = Field(
        default=None,
        description="Optional. Only fetch messages with accept_time after this date.",
    )
    end_time: Optional[datetime] = Field(
        default=None,
        description="Optional. Only fetch messages with accept_time before this date.",
    )
    channel: Optional[ConversationChannelType] = Field(
        default=None,
        description="Optional. Only fetch messages from the channel.",
    )
    direction: Optional[ConversationDirectionType] = Field(
        default=None,
        description="Optional. Only fetch messages with the specified direction. If direction is not specified, it will list both TO_APP and TO_CONTACT messages.",
    )
