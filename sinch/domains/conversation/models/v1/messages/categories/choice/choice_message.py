from typing import Optional
from pydantic import Field, conlist
from sinch.domains.conversation.models.v1.messages.categories.choice.choice_option import (
    ChoiceOption,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.messages.categories.text import (
    TextMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.card.message_properties import (
    MessageProperties,
)


class ChoiceMessage(BaseModelConfiguration):
    choices: conlist(ChoiceOption) = Field(
        default=..., description="The number of choices is limited to 10."
    )
    text_message: Optional[TextMessage] = None
    message_properties: Optional[MessageProperties] = None
