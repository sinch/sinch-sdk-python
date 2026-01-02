from typing import Union
from sinch.domains.conversation.models.v1.messages.categories.app.app_message import (
    CardAppMessage,
    CarouselAppMessage,
    ChoiceAppMessage,
    ContactInfoAppMessage,
    ListAppMessage,
    LocationAppMessage,
    MediaAppMessage,
    TemplateAppMessage,
    TextAppMessage,
)

AppMessage = Union[
    CardAppMessage,
    CarouselAppMessage,
    ChoiceAppMessage,
    LocationAppMessage,
    MediaAppMessage,
    TemplateAppMessage,
    TextAppMessage,
    ListAppMessage,
    ContactInfoAppMessage,
]
