from pydantic import Field

from sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.contact.contact_merge_notification import (
    ContactMergeNotification,
)


class ContactMergeEvent(ConversationSinchEventBase):
    """Sinch Event for CONTACT_MERGE (two contacts are merged)."""

    contact_merge_notification: ContactMergeNotification = Field(
        description="The contact merge notification payload."
    )
