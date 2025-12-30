from typing import Union
from sinch.domains.conversation.models.v1.messages.response.conversation_message import (
    AppMessageConversationMessage,
    ContactMessageConversationMessage,
)


ConversationMessageResponse = Union[
    AppMessageConversationMessage,
    ContactMessageConversationMessage,
]
