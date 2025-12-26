from typing import Optional
from pydantic import Field, StrictStr, conlist
from sinch.domains.conversation.models.v1.messages.types.list_item_one_of_internal import (
    ListItemOneOfInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ListSection(BaseModelConfigurationResponse):
    title: Optional[StrictStr] = Field(
        default=None, description="Optional parameter. Title for list section."
    )
    items: conlist(ListItemOneOfInternal) = Field(...)
