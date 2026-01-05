from typing import Optional
from pydantic import Field, StrictStr, conlist
from sinch.domains.conversation.models.v1.messages.response.types.list_item import (
    ListItem,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ListSection(BaseModelConfigurationResponse):
    title: Optional[StrictStr] = Field(
        default=None, description="Optional parameter. Title for list section."
    )
    items: conlist(ListItem) = Field(...)
