from typing import Optional, Literal
from pydantic import Field, StrictStr
from sinch.domains.numbers.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class VoiceConfigurationRTC(BaseModelConfigurationRequest):
    type: Literal["RTC"] = "RTC"
    app_id: Optional[StrictStr] = Field(default=None, alias="appId")
