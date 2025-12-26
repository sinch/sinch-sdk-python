from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class MessagePropertiesInternal(BaseModelConfigurationResponse):
    whatsapp_header: Optional[StrictStr] = Field(
        default=None,
        description=(
            "Optional. Sets the header text for a WhatsApp reply button message when there is no media. "
            "Ignored for other channels or when not transcoded to native WhatsApp reply buttons."
        ),
    )
