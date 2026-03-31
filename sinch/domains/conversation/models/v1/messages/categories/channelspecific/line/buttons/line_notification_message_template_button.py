from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class LineNotificationMessageTemplateButton(BaseModelConfiguration):
    button_key: StrictStr = Field(
        ...,
        description="Button key. See LINE documentation for available keys.",
    )
    url: StrictStr = Field(..., description="Button URL.")
