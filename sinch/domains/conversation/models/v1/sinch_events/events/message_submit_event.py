from pydantic import Field

from sinch.domains.conversation.models.v1.sinch_events.events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.events.message_submit_notification import (
    MessageSubmitNotification,
)


class MessageSubmitEvent(ConversationSinchEventBase):
    """Sinch Event for MESSAGE_SUBMIT (message submission notification)."""

    message_submit_notification: MessageSubmitNotification = Field(
        description="The message submit notification payload.",
    )
