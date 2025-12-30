from typing import Optional
from sinch.domains.conversation.models.v1.messages.response.shared.list_message import (
    ListMessage,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ListMessageField(BaseModelConfigurationResponse):
    list_message: Optional[ListMessage] = None
