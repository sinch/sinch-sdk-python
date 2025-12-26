from typing import Optional
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.conversation.models.v1.messages.shared.text_message_internal import (
    TextMessageInternal,
)


class TextMessageFieldInternal(BaseModelConfigurationResponse):
    text_message: Optional[TextMessageInternal] = None
