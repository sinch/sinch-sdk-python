from typing import Optional

from pydantic import Field

from sinch.domains.conversation.models.v1.conversations.response.conversation_response import (
    ConversationResponse,
)
from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent


class ConversationNotification(SinchEvent):
    """Object containing the details of the started / stopped / deleted conversation"""

    conversation: Optional[ConversationResponse] = Field(
        default=None, description="The conversation."
    )
