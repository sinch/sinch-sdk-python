from typing import Literal
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class WhatsAppInteractiveTextHeader(BaseModelConfigurationResponse):
    type: Literal["text"] = Field(..., description="The text of the header.")
    text: StrictStr = Field(
        ...,
        description="Text for the header. Formatting allows emojis, but not Markdown.",
    )
