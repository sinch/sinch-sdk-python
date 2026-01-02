from typing import Union
from sinch.domains.conversation.models.v1.messages.response.message_response import (
    AppMessageResponse,
    ContactMessageResponse,
)


ConversationMessageResponse = Union[
    AppMessageResponse,
    ContactMessageResponse,
]
