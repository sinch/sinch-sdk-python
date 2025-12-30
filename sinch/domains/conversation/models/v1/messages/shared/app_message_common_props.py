from typing import Dict, Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.response.shared.channel_specific_message import (
    ChannelSpecificMessage,
)
from sinch.domains.conversation.models.v1.messages.shared import Agent
from sinch.domains.conversation.models.v1.messages.response.shared.omni_message_override import (
    OmniMessageOverride,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class AppMessageCommonProps(BaseModelConfigurationResponse):
    explicit_channel_message: Optional[Dict[str, StrictStr]] = Field(
        default=None,
        description="Allows you to specify a channel and define a corresponding channel specific message payload that will override the standard Conversation API message types. The key in the map must point to a valid conversation channel as defined in the enum `ConversationChannel`. The message content must be provided in string format. You may use the [transcoding endpoint](https://developers.sinch.com/docs/conversation/api-reference/conversation/tag/Transcoding/) to help create your message. For more information about how to construct an explicit channel message for a particular channel, see that [channel's corresponding documentation](https://developers.sinch.com/docs/conversation/channel-support/) (for example, using explicit channel messages with [the WhatsApp channel](https://developers.sinch.com/docs/conversation/channel-support/whatsapp/message-support/#explicit-channel-messages)).",
    )
    explicit_channel_omni_message: Optional[Dict[str, OmniMessageOverride]] = (
        Field(
            default=None,
            description="Override the message's content for specified channels. The key in the map must point to a valid conversation channel as defined in the enum `ConversationChannel`. The content defined under the specified channel will be sent on that channel.",
        )
    )
    channel_specific_message: Optional[Dict[str, ChannelSpecificMessage]] = (
        Field(
            default=None,
            description="Channel specific messages, overriding any transcoding. The structure of this property is more well-defined than the open structure of the `explicit_channel_message` property, and may be easier to use. The key in the map must point to a valid conversation channel as defined in the enum `ConversationChannel`.",
        )
    )
    agent: Optional[Agent] = None
