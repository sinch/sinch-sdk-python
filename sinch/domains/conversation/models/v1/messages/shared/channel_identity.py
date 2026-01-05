from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.types.conversation_channel_type import (
    ConversationChannelType,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ChannelIdentity(BaseModelConfigurationResponse):
    app_id: Optional[StrictStr] = Field(
        default=None,
        description="Required if using a channel that uses app-scoped channel identities. Currently, FB Messenger, Instagram, LINE, and WeChat use app-scoped channel identities, which means contacts will have different channel identities on different Conversation API apps. These can be thought of as virtual identities that are app-specific and, therefore, the app_id must be included in the API call.",
    )
    channel: ConversationChannelType = Field(...)
    identity: StrictStr = Field(
        default=...,
        description="The channel identity. This will differ from channel to channel. For example, a phone number for SMS, WhatsApp, and Viber Business.",
    )
