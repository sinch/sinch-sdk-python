from pydantic import Field

from sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.conversation.conversation_notification import (
    ConversationNotification,
)


class ConversationStopEvent(ConversationSinchEventBase):
    """Sinch Event for CONVERSATION_STOP (a conversation between the subscribed app and a contact is stopped)."""

    conversation_stop_notification: ConversationNotification = Field(
        description="The conversation stop notification payload."
    )
