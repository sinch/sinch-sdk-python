from pydantic import Field
from sinch.domains.conversation.models.v1.messages.shared.choice_item import (
    ChoiceItem,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class ListItemChoice(BaseModelConfiguration):
    choice: ChoiceItem = Field(...)
