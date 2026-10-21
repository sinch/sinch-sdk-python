from pydantic import Field

from sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.channel.channel_event_notification import (
    ChannelEventNotification,
)


class ChannelEvent(ConversationSinchEventBase):
    """Sinch Event for CHANNEL_EVENT (notification of channel-specific information and updates, for example a WhatsApp quality rating change)."""

    channel_event_notification: ChannelEventNotification = Field(
        description="The channel event notification payload."
    )
