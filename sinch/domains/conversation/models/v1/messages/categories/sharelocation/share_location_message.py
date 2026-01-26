from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class ShareLocationMessage(BaseModelConfiguration):
    title: StrictStr = Field(
        ...,
        description="The title is shown close to the button that leads to open a map to share a location.",
    )
    fallback_url: StrictStr = Field(
        ...,
        description="The URL that is opened when channel does not have support for this type.",
    )
