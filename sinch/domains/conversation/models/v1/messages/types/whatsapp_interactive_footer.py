from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class WhatsAppInteractiveFooter(BaseModelConfigurationResponse):
    text: StrictStr = Field(
        ...,
        description="The footer content (60 characters maximum). Emojis, Markdown and links are supported.",
    )
