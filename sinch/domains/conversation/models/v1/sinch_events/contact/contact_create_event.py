from pydantic import Field

from sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.contact.contact_notification import (
    ContactNotification,
)


class ContactCreateEvent(ConversationSinchEventBase):
    """Sinch Event for CONTACT_CREATE (a new contact is created)."""

    contact_create_notification: ContactNotification = Field(
        description="The contact create notification payload."
    )
