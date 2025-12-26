from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class MediaPropertiesInternal(BaseModelConfigurationResponse):
    thumbnail_url: Optional[StrictStr] = Field(
        default=None,
        description="An optional parameter. Will be used where it is natively supported.",
    )
    url: StrictStr = Field(default=..., description="Url to the media file.")
    filename_override: Optional[StrictStr] = Field(
        default=None, description="Overrides the media file name."
    )
