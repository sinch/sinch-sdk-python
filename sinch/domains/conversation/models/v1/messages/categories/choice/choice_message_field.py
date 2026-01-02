from typing import Optional
from sinch.domains.conversation.models.v1.messages.categories.choice.choice_message import (
    ChoiceMessage,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ChoiceMessageField(BaseModelConfigurationResponse):
    choice_message: Optional[ChoiceMessage] = None
