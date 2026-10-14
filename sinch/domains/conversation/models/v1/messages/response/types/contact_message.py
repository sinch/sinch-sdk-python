from typing import Annotated, Union
from sinch.core.models.internal.unions import ResolveUnion
from sinch.domains.conversation.models.v1.messages.categories.contact.contact_message import (
    ChannelSpecificContactMessage,
    ChoiceResponseContactMessage,
    FallbackContactMessage,
    LocationContactMessage,
    MediaCardContactMessage,
    MediaContactMessage,
    ProductResponseContactMessage,
    TextContactMessage,
)

ContactMessage = Annotated[
    Union[
        ChannelSpecificContactMessage,
        ChoiceResponseContactMessage,
        FallbackContactMessage,
        LocationContactMessage,
        MediaCardContactMessage,
        MediaContactMessage,
        ProductResponseContactMessage,
        TextContactMessage,
    ],
    ResolveUnion(),
]
