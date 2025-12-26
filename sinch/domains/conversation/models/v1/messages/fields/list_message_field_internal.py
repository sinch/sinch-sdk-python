from typing import Optional
from sinch.domains.conversation.models.v1.messages.types.list_message_internal import (
    ListMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ListMessageFieldInternal(BaseModelConfigurationResponse):
    list_message: Optional[ListMessageInternal] = None
