from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.types.conversation_channel_type import (
    ConversationChannelType,
)


class ChannelIdentity(BaseModelConfiguration):
    app_id: Optional[StrictStr] = Field(
        default=None,
        description="Required if using a channel that uses app-scoped channel identities. Currently, FB Messenger, Instagram, LINE, and WeChat use app-scoped channel identities, which means contacts will have different channel identities on different Conversation API apps. These can be thought of as virtual identities that are app-specific and, therefore, the app_id must be included in the API call.",
    )
    channel: ConversationChannelType = Field(
        description="The identifier of the channel you want to include. Must be one of the enum values."
    )
    identity: StrictStr = Field(
        description="The channel identity. This will differ from channel to channel. For example, a phone number for SMS, WhatsApp, and Viber Business."
    )
