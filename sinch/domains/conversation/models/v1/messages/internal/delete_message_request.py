from typing import Optional
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.types import (
    MessagesSourceType,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationRequest,
)


class DeleteMessageRequest(BaseModelConfigurationRequest):
    message_id: str = Field(...)
    messages_source: Optional[MessagesSourceType] = None
