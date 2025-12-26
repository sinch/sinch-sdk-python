from typing import Optional
from sinch.domains.conversation.models.v1.messages.shared.card_message_internal import (
    CardMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class CardMessageFieldInternal(BaseModelConfigurationResponse):
    card_message: Optional[CardMessageInternal] = None
