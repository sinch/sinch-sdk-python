from typing import Literal, Optional, Union
from pydantic import Field, StrictStr, StrictInt
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)


class MOMediaItem(BaseModelConfigurationResponse):
    url: Optional[StrictStr] = Field(default=None, description="URL to the media file.")
    content_type: StrictStr = Field(
        ..., description="Content type of the media file."
    )
    status: Union[Literal["Uploaded", "Failed"], StrictStr] = Field(
        ..., description="Status of the media upload."
    )
    code: StrictInt = Field(..., description="The result code.")
