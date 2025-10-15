from typing import Optional, Literal
from pydantic import Field, StrictStr
from sinch.domains.numbers.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class VoiceConfigurationEST(BaseModelConfigurationRequest):
    type: Literal["EST"] = "EST"
    trunk_id: Optional[StrictStr] = Field(default=None, alias="trunkId")
