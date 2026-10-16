from typing import Optional

from pydantic import Field, StrictInt, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ListEventsRequest(BaseModelConfiguration):
    conversation_id: Optional[StrictStr] = Field(
        default=None,
        description="Resource name (id) of the conversation. One of conversation_id or contact_id needs to be present.",
    )
    contact_id: Optional[StrictStr] = Field(
        default=None,
        description="Resource name (id) of the contact. One of conversation_id or contact_id needs to be present.",
    )
    page_size: Optional[StrictInt] = Field(
        default=None,
        description="Maximum number of events to fetch. Defaults to 10 and the maximum is 20.",
    )
    page_token: Optional[StrictStr] = Field(
        default=None,
        description="Next page token previously returned if any. When specifying this token, make sure to use the same values for the other parameters from the request that originated the token, otherwise the paged results may be inconsistent.",
    )
