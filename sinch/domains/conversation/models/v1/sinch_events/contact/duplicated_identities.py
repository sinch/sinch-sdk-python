from typing import Optional

from pydantic import Field, StrictStr, conlist

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent
from sinch.domains.conversation.models.v1.types.conversation_channel_type import (
    ConversationChannelType,
)


class DuplicatedIdentities(SinchEvent):
    channel: Optional[ConversationChannelType] = None
    contact_ids: Optional[conlist(StrictStr)] = Field(
        default=None,
        description="List of duplicated ids in the specified channel.",
    )
