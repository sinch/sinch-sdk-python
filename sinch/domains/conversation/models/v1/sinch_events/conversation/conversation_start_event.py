from pydantic import Field

from sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.conversation.conversation_notification import (
    ConversationNotification,
)


class ConversationStartEvent(ConversationSinchEventBase):
    """Sinch Event for CONVERSATION_START (a new conversation between the subscribed app and a contact is started)."""

    conversation_start_notification: ConversationNotification = Field(
        description="The conversation start notification payload."
    )
