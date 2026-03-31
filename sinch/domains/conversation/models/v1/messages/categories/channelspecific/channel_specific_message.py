from pydantic import Field
from sinch.domains.conversation.models.v1.messages.types.channel_specific_message_type import (
    ChannelSpecificMessageType,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.channel_specific_message_content import (
    ChannelSpecificMessageContent,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class ChannelSpecificMessage(BaseModelConfiguration):
    message_type: ChannelSpecificMessageType = Field(
        ..., description="The type of the channel specific message."
    )
    message: ChannelSpecificMessageContent = Field(...)
