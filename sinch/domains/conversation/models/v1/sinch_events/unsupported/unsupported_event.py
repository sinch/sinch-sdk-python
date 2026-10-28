from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.shared.channel_identity import (
    ChannelIdentity,
)
from sinch.domains.conversation.models.v1.types.conversation_channel_type import (
    ConversationChannelType,
)
from sinch.domains.conversation.models.v1.types.processing_mode_type import (
    ProcessingModeType,
)
from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent


class UnsupportedEvent(SinchEvent):
    channel: Optional[ConversationChannelType] = None
    payload: Optional[StrictStr] = Field(
        default=None,
        description="Normally a JSON payload as sent by the channel.",
    )
    processing_mode: Optional[ProcessingModeType] = None
    id: Optional[StrictStr] = Field(
        default=None, description="The message ID."
    )
    contact_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the contact. This field is blank if not supported.",
    )
    conversation_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the conversation this message is part of. This field is blank if not supported.",
    )
    channel_identity: Optional[ChannelIdentity] = None
