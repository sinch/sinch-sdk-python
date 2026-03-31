from typing import Optional
from sinch.domains.conversation.models.v1.messages.categories.choice.choice_message import (
    ChoiceMessage,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class ChoiceMessageField(BaseModelConfiguration):
    choice_message: Optional[ChoiceMessage] = None
