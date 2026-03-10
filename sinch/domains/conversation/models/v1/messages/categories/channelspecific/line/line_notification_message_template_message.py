from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.line.line_notification_message_template_body import (
    LineNotificationMessageTemplateBody,
)


class LineNotificationMessageTemplateMessage(BaseModelConfiguration):
    template_key: StrictStr = Field(
        ...,
        description="Template key. See LINE documentation for available keys.",
    )
    body: Optional[LineNotificationMessageTemplateBody] = Field(
        default=None, description="Template body."
    )
