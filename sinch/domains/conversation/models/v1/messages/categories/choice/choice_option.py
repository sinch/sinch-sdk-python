from typing import Union

from sinch.domains.conversation.models.v1.messages.categories.choice.choice_options import (
    CalendarChoiceMessage,
    CallChoiceMessage,
    LocationChoiceMessage,
    ShareLocationChoiceMessage,
    TextChoiceMessage,
    UrlChoiceMessage,
)

ChoiceOption = Union[
    CallChoiceMessage,
    LocationChoiceMessage,
    TextChoiceMessage,
    UrlChoiceMessage,
    CalendarChoiceMessage,
    ShareLocationChoiceMessage,
]
