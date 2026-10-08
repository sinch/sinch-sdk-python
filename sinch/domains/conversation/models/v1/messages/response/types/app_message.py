from typing import Annotated, Union
from sinch.core.models.internal.unions import ResolveUnion
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

AppMessage = Annotated[
    Union[
        CardAppMessage,
        CarouselAppMessage,
        ChoiceAppMessage,
        ContactInfoAppMessage,
        ListAppMessage,
        LocationAppMessage,
        MediaAppMessage,
        TemplateAppMessage,
        TextAppMessage,
    ],
    ResolveUnion(),
]
