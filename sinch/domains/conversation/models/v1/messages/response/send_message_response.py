from datetime import datetime
from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class SendMessageResponse(BaseModelConfiguration):
    accepted_time: Optional[datetime] = Field(
        default=None,
        description="Timestamp when the Conversation API accepted the message for delivery to the referenced contact.",
    )
    message_id: StrictStr = Field(
        ...,
        description="The ID of the sent message.",
    )
