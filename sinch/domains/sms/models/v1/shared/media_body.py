from typing import Optional
from pydantic import Field, constr
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)


class MediaBody(BaseModelConfigurationResponse):
    subject: Optional[constr(strict=True, max_length=80, min_length=0)] = (
        Field(default=None, description="The subject text")
    )
    message: Optional[constr(strict=True, max_length=2000, min_length=0)] = (
        Field(
            default=None,
            description="The message text. Text only media messages will be rejected, please use SMS instead.",
        )
    )
    url: constr(strict=True, max_length=2048, min_length=0) = Field(
        default=..., description="URL to the media file"
    )
