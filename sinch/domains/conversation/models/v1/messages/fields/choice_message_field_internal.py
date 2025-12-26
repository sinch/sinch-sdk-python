from typing import Optional
from sinch.domains.conversation.models.v1.messages.types.choice_message_internal import (
    ChoiceMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ChoiceMessageFieldInternal(BaseModelConfigurationResponse):
    choice_message: Optional[ChoiceMessageInternal] = None
