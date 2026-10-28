from pydantic import Field

from sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.conversation.conversation_notification import (
    ConversationNotification,
)


class ConversationDeleteEvent(ConversationSinchEventBase):
    """Sinch Event for CONVERSATION_DELETE (a conversation between the subscribed app and a contact is deleted)."""

    conversation_delete_notification: ConversationNotification = Field(
        description="The conversation delete notification payload."
    )
