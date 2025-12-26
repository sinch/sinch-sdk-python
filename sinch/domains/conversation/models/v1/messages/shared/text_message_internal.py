from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class TextMessageInternal(BaseModelConfigurationResponse):
    text: StrictStr = Field(
        ..., description="The text content of the message."
    )
