from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.types.conversation_channel_type import (
    ConversationChannelType,
)
from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.analysis_result import (
    AnalysisResult,
)


class SmartConversationNotification(SinchEvent):
    contact_id: Optional[StrictStr] = Field(
        default=None,
        description="The unique ID of the contact that sent the message.",
    )
    channel_identity: Optional[StrictStr] = Field(
        default=None,
        description="The channel-specific identifier for the contact.",
    )
    channel: Optional[ConversationChannelType] = None
    message_id: Optional[StrictStr] = Field(
        default=None, description="The unique ID of the corresponding message."
    )
    conversation_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the conversation the app message is part of.",
    )
    analysis_results: Optional[AnalysisResult] = Field(default=None)
