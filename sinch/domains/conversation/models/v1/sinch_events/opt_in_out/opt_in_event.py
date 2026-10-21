from pydantic import Field

from sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.opt_in_out.opt_in_notification import (
    OptInNotification,
)


class OptInEvent(ConversationSinchEventBase):
    """Sinch Event for OPT_IN (opt-in notification from the channels)."""

    opt_in_notification: OptInNotification = Field(
        description="The opt-in notification payload."
    )
