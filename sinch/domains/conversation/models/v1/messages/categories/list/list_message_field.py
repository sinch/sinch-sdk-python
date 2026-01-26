from typing import Optional
from sinch.domains.conversation.models.v1.messages.categories.list.list_message import (
    ListMessage,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class ListMessageField(BaseModelConfiguration):
    list_message: Optional[ListMessage] = None
