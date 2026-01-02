from typing import Optional
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.conversation.models.v1.messages.categories.text import (
    TextMessage,
)


class TextMessageField(BaseModelConfigurationResponse):
    text_message: Optional[TextMessage] = None
