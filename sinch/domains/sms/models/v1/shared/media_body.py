from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)


class MediaBody(BaseModelConfigurationResponse):
    subject: Optional[StrictStr] = Field(
        default=None, description="The subject text"
    )
    message: Optional[StrictStr] = Field(
        default=None,
        description="The message text. Text only media messages will be rejected, please use SMS instead.",
    )
    url: StrictStr = Field(default=..., description="URL to the media file")
