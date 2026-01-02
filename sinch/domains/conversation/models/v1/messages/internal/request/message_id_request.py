from typing import Optional
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.types import (
    MessagesSourceType,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationRequest,
)


class MessageIdRequest(BaseModelConfigurationRequest):
    message_id: str = Field(..., description="The unique ID of the message.")
    messages_source: Optional[MessagesSourceType] = Field(
        default=None,
        description="Specifies the message source for which the request will be processed. Used for operations on messages in Dispatch Mode. For more information, see [Processing Modes](https://developers.sinch.com/docs/conversation/processing-modes/).",
    )
