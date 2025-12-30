from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ReplyTo(BaseModelConfigurationResponse):
    message_id: StrictStr = Field(
        default=...,
        description="Required. The Id of the message that this is a response to",
    )
