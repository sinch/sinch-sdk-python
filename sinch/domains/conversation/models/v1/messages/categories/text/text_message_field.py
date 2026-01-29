from typing import Optional
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.messages.categories.text import (
    TextMessage,
)


class TextMessageField(BaseModelConfiguration):
    text_message: Optional[TextMessage] = None
