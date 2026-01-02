from typing import Union
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

ContactMessage = Union[
    ChannelSpecificContactMessage,
    ChoiceResponseContactMessage,
    FallbackContactMessage,
    LocationContactMessage,
    MediaCardContactMessage,
    MediaContactMessage,
    ProductResponseContactMessage,
    TextContactMessage,
]
