from pydantic import Field

from sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.opt_in_out.opt_out_notification import (
    OptOutNotification,
)


class OptOutEvent(ConversationSinchEventBase):
    """Sinch Event for OPT_OUT (opt-out notification from the channels)."""

    opt_out_notification: OptOutNotification = Field(
        description="The opt-out notification payload."
    )
