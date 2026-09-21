from typing import Literal, Optional

from pydantic import Field, StrictStr

from sinch.domains.numbers.models.v1.shared.voice_configuration_common import (
    VoiceConfigurationCommon,
)


class VoiceConfigurationEST(VoiceConfigurationCommon):
    trunk_id: Optional[StrictStr] = Field(default=None, alias="trunkId")
    type: Literal["EST"] = Field(default="EST", alias="type")
