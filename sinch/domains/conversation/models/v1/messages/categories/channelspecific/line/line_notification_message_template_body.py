from typing import Optional
from pydantic import Field, conlist
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.line.line_notification_message_template_emphasized_item import (
    LineNotificationMessageTemplateEmphasizedItem,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.line.line_notification_message_template_item import (
    LineNotificationMessageTemplateItem,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.line.buttons import (
    LineNotificationMessageTemplateButton,
)


class LineNotificationMessageTemplateBody(BaseModelConfiguration):
    emphasized_item: Optional[
        LineNotificationMessageTemplateEmphasizedItem
    ] = Field(default=None, description="Template emphasized item.")
    items: Optional[conlist(LineNotificationMessageTemplateItem)] = Field(
        default=None, description="List of template items."
    )
    buttons: Optional[conlist(LineNotificationMessageTemplateButton)] = Field(
        default=None, description="List of template buttons."
    )
