from typing import List, Optional

from pydantic import Field, StrictInt, StrictStr, conlist

from sinch.domains.conversation.models.v1.conversations.response.recent_conversation_response import (
    RecentConversationResponse,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ListRecentConversationsResponse(BaseModelConfiguration):
    conversations: Optional[conlist(RecentConversationResponse)] = Field(
        default=None, description="List of recent conversations"
    )
    next_page_token: Optional[StrictStr] = Field(
        default=None,
        description="Token that should be included in the next request to fetch the next page.",
    )
    total_size: Optional[StrictInt] = None

    @property
    def content(self) -> List[RecentConversationResponse]:
        return self.conversations or []
