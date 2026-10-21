from pydantic import Field

from sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.inbound.inbound_event import (
    InboundEvent,
)


class EventInboundEvent(ConversationSinchEventBase):
    """Sinch Event for EVENT_INBOUND (inbound event from user)."""

    event: InboundEvent = Field(description="The inbound event payload.")
