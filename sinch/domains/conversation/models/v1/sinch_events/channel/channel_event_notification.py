from typing import Optional

from pydantic import Field

from sinch.domains.conversation.models.v1.sinch_events.channel.channel_event_details import (
    ChannelEventDetails,
)
from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent


class ChannelEventNotification(SinchEvent):
    channel_event: Optional[ChannelEventDetails] = Field(
        default=None, description="The channel event."
    )
