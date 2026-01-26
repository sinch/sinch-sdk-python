from typing import Optional
from sinch.domains.conversation.models.v1.messages.categories.common.reply_to import (
    ReplyTo,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class ContactMessageCommonProps(BaseModelConfiguration):
    reply_to: Optional[ReplyTo] = None
