from typing import List, Optional

from pydantic import Field, StrictInt, StrictStr, conlist

from sinch.domains.conversation.models.v1.conversations.response.conversation_response import (
    ConversationResponse,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ListConversationsResponse(BaseModelConfiguration):
    conversations: Optional[conlist(ConversationResponse)] = Field(
        default=None,
        description="List of conversations matching the search query.",
    )
    next_page_token: Optional[StrictStr] = Field(
        default=None,
        description="Token that should be included in the next request to fetch the next page.",
    )
    total_size: Optional[StrictInt] = None

    @property
    def content(self) -> List[ConversationResponse]:
        return self.conversations or []
