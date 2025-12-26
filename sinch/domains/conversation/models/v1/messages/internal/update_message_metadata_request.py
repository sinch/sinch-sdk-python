from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.types import (
    MessagesSourceType,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationRequest,
)


class UpdateMessageMetadataRequest(BaseModelConfigurationRequest):
    message_id: str = Field(..., description="The unique ID of the message.")
    metadata: StrictStr = Field(
        ..., description="Metadata that should be associated with the message."
    )
    messages_source: Optional[MessagesSourceType] = Field(
        default=None,
        description="Specifies the message source for which the request will be processed. Used for operations on messages in Dispatch Mode.",
    )
