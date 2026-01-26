from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class UrlMessage(BaseModelConfiguration):
    title: StrictStr = Field(
        default=...,
        description="The title shown close to the URL. The title can be clickable in some cases.",
    )
    url: StrictStr = Field(default=..., description="The url to show.")
