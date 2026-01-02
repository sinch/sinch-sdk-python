from typing import Optional
from sinch.domains.conversation.models.v1.messages.categories.card.card_message import (
    CardMessage,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class CardMessageField(BaseModelConfigurationResponse):
    card_message: Optional[CardMessage] = None
