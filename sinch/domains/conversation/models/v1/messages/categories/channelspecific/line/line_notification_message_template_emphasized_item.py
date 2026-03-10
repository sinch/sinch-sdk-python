from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class LineNotificationMessageTemplateEmphasizedItem(BaseModelConfiguration):
    item_key: StrictStr = Field(
        ...,
        description="Item key. See LINE documentation for available keys.",
    )
    content: StrictStr = Field(..., description="Item value.")
