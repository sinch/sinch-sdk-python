from pydantic import Field

from sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.capability.capability_notification import (
    CapabilityNotification,
)


class CapabilityEvent(ConversationSinchEventBase):
    """Sinch Event for CAPABILITY (result of an asynchronous capability check)."""

    capability_notification: CapabilityNotification = Field(
        description="The capability notification payload."
    )
