from typing import Optional
from sinch.domains.conversation.models.v1.messages.shared.reply_to_internal import (
    ReplyToInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ContactMessageCommonProps(BaseModelConfigurationResponse):
    reply_to: Optional[ReplyToInternal] = None
