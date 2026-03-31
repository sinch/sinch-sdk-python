from typing import List, Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.messages.response.types import (
    ConversationMessageResponse,
)


class ListMessagesResponse(BaseModelConfiguration):
    messages: Optional[List[ConversationMessageResponse]] = Field(
        default=None,
        description="List of messages associated to the referenced conversation.",
    )
    next_page_token: Optional[StrictStr] = Field(
        default=None,
        description="Token that should be included in the next request to fetch the next page.",
    )

    @property
    def content(self):
        """Returns the messages as part of the response object for pagination compatibility."""
        return self.messages or []
