from typing import List, Optional

from pydantic import Field, StrictStr, conlist

from sinch.domains.conversation.models.v1.events.response.conversation_event_response import (
    ConversationEventResponse,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ListEventsResponse(BaseModelConfiguration):
    events: Optional[conlist(ConversationEventResponse)] = Field(
        default=None, description="List of ConversationsEvents."
    )
    next_page_token: Optional[StrictStr] = Field(
        default=None,
        description="Token that should be included in the next request to fetch the next page.",
    )

    @property
    def content(self) -> List[ConversationEventResponse]:
        return self.events or []
