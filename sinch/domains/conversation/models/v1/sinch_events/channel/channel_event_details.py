from typing import Any, Dict, Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.types.conversation_channel_type import (
    ConversationChannelType,
)
from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent


class ChannelEventDetails(SinchEvent):
    channel: Optional[ConversationChannelType] = None
    event_type: Optional[StrictStr] = Field(
        default=None, description="The type of event being reported."
    )
    additional_data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="An object containing additional information regarding the event. The contents of the object depend on the channel and the event_type.",
    )
