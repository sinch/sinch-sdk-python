from typing import Annotated, Union
from sinch.core.models.internal.unions import ResolveUnion
from sinch.domains.conversation.models.v1.messages.response.message_response import (
    AppMessageResponse,
    ContactMessageResponse,
)


ConversationMessageResponse = Annotated[
    Union[
        AppMessageResponse,
        ContactMessageResponse,
    ],
    ResolveUnion(),
]
