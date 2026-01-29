from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class UrlInfo(BaseModelConfiguration):
    url: StrictStr = Field(default=..., description="The URL to be referenced")
    type: Optional[StrictStr] = Field(
        default=None, description="Optional. URL type, e.g. Org or Social"
    )
