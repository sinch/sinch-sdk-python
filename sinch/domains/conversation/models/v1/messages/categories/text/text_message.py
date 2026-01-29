from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class TextMessage(BaseModelConfiguration):
    text: StrictStr = Field(
        ..., description="The text content of the message."
    )
