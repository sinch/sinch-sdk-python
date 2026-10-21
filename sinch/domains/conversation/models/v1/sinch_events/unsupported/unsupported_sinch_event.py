from pydantic import Field

from sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.unsupported.unsupported_event import (
    UnsupportedEvent,
)


class UnsupportedSinchEvent(ConversationSinchEventBase):
    """Sinch Event for UNSUPPORTED (events received from the channels that have no native mapping in the Conversation API yet)."""

    unsupported_event: UnsupportedEvent = Field(
        alias="unsupported_callback",
        description="The unsupported event payload.",
    )
