from pydantic import Field

from sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.contact.contact_notification import (
    ContactNotification,
)


class ContactDeleteEvent(ConversationSinchEventBase):
    """Sinch Event for CONTACT_DELETE (a contact is deleted)."""

    contact_delete_notification: ContactNotification = Field(
        description="The contact delete notification payload."
    )
