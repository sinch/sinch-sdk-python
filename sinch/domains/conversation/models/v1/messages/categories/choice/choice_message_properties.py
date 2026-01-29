from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class ChoiceMessageProperties(BaseModelConfiguration):
    whatsapp_footer: Optional[StrictStr] = Field(
        default=None,
        description=(
            "Optional. Sets the text for the footer of a WhatsApp reply button or URL button message. "
            "Ignored for other channels."
        ),
    )
