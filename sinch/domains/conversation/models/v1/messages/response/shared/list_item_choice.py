from pydantic import Field
from sinch.domains.conversation.models.v1.messages.shared.choice_item import (
    ChoiceItem,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ListItemChoice(BaseModelConfigurationResponse):
    choice: ChoiceItem = Field(...)
