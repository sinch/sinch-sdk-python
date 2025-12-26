from pydantic import Field
from sinch.domains.conversation.models.v1.messages.types.channel_specific_message_type import (
    ChannelSpecificMessageType,
)
from sinch.domains.conversation.models.v1.messages.types.channel_specific_message_content_internal import (
    ChannelSpecificMessageContentInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ChannelSpecificMessageInternal(BaseModelConfigurationResponse):
    message_type: ChannelSpecificMessageType = Field(
        ..., description="The type of the channel specific message."
    )
    message: ChannelSpecificMessageContentInternal = Field(...)
