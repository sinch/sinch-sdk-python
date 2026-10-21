from pydantic import Field

from sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.contact.contact_notification import (
    ContactNotification,
)


class ContactUpdateEvent(ConversationSinchEventBase):
    """Sinch Event for CONTACT_UPDATE (a contact is updated)."""

    contact_update_notification: ContactNotification = Field(
        description="The contact update notification payload."
    )
