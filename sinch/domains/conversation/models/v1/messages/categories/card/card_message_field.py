from typing import Optional
from sinch.domains.conversation.models.v1.messages.categories.card.card_message import (
    CardMessage,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class CardMessageField(BaseModelConfiguration):
    card_message: Optional[CardMessage] = None
