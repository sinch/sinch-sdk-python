from pydantic import Field

from sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.record.record_notification import (
    RecordNotification,
)


class RecordNotificationEvent(ConversationSinchEventBase):
    """Sinch Event for RECORD_NOTIFICATION (record notification for an entity)."""

    record_notification: RecordNotification = Field(
        description="The record notification payload."
    )
