from pydantic import Field

from sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.smart_conversation_notification import (
    SmartConversationNotification,
)


class SmartConversationsEvent(ConversationSinchEventBase):
    """Sinch Event for SMART_CONVERSATION (Machine Learning and Artificial Intelligence analyses of the Smart Conversations functionality)."""

    smart_conversation_notification: SmartConversationNotification = Field(
        description="The smart conversation notification payload."
    )
