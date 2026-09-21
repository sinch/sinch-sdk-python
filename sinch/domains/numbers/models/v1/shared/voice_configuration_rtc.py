from typing import Literal, Optional

from pydantic import Field, StrictStr

from sinch.domains.numbers.models.v1.shared.voice_configuration_common import (
    VoiceConfigurationCommon,
)


class VoiceConfigurationRTC(VoiceConfigurationCommon):
    app_id: Optional[StrictStr] = Field(default=None, alias="appId")
    type: Literal["RTC"] = Field(default="RTC", alias="type")
