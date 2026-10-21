from pydantic import Field

from sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.contact.duplicated_contact_identities_notification import (
    DuplicatedContactIdentitiesNotification,
)


class ContactIdentitiesDuplicationEvent(ConversationSinchEventBase):
    """Sinch Event for CONTACT_IDENTITIES_DUPLICATION (duplicates of channel identities are found between multiple contacts during message and event processing)."""

    duplicated_contact_identities_notification: DuplicatedContactIdentitiesNotification = Field(
        description="The duplicated contact identities notification payload."
    )
