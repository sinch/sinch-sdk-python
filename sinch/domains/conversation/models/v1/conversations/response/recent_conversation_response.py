from typing import Optional

from sinch.domains.conversation.models.v1.conversations.response.conversation_response import (
    ConversationResponse,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.messages.response.types.conversation_message_response import (
    ConversationMessageResponse,
)


class RecentConversationResponse(BaseModelConfiguration):
    conversation: Optional[ConversationResponse] = None
    last_message: Optional[ConversationMessageResponse] = None
