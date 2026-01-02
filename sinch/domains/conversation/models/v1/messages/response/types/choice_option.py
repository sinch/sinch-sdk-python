from typing import Union
from sinch.domains.conversation.models.v1.messages.categories.choice.choice_options import (
    CallChoiceMessage,
    LocationChoiceMessage,
    TextChoiceMessage,
    UrlChoiceMessage,
    CalendarChoiceMessage,
    ShareLocationChoiceMessage,
)


ChoiceOption = Union[
    CallChoiceMessage,
    LocationChoiceMessage,
    TextChoiceMessage,
    UrlChoiceMessage,
    CalendarChoiceMessage,
    ShareLocationChoiceMessage,
]
