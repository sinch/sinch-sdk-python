from typing import Optional
from sinch.domains.conversation.models.v1.messages.categories.common.reply_to import (
    ReplyTo,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ContactMessageCommonProps(BaseModelConfigurationResponse):
    reply_to: Optional[ReplyTo] = None
