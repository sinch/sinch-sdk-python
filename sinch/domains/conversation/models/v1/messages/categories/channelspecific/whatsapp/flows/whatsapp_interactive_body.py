from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class WhatsAppInteractiveBody(BaseModelConfigurationResponse):
    text: StrictStr = Field(
        ...,
        description="The content of the message (1024 characters maximum). Emojis and Markdown are supported.",
    )
