from pydantic import Field

from sinch.domains.conversation.models.v1.sinch_events.events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.events.inbound_message import (
    InboundMessage,
)


class MessageInboundEvent(ConversationSinchEventBase):
    """Sinch Event for MESSAGE_INBOUND (inbound message from user)."""

    message: InboundMessage = Field(
        description="The inbound message payload.",
    )
