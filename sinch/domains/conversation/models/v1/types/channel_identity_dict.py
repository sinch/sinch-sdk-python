from typing import TypedDict

from typing_extensions import NotRequired

from sinch.domains.conversation.models.v1.types.conversation_channel_type import (
    ConversationChannelType,
)


class ChannelIdentityDict(TypedDict):
    channel: ConversationChannelType
    identity: str
    app_id: NotRequired[str]
