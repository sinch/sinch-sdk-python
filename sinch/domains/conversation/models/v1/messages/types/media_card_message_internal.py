from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class MediaCardMessageInternal(BaseModelConfigurationResponse):
    caption: Optional[StrictStr] = Field(
        default=None,
        description="Caption for the media on supported channels.",
    )
    url: StrictStr = Field(default=..., description="Url to the media file.")
