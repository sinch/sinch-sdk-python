from typing import Literal, Optional

from pydantic import Field, StrictStr

from sinch.domains.numbers.models.v1.shared.voice_configuration_common import (
    VoiceConfigurationCommon,
)


class VoiceConfigurationFAX(VoiceConfigurationCommon):
    service_id: Optional[StrictStr] = Field(default=None, alias="serviceId")
    type: Literal["FAX"] = Field(default="FAX", alias="type")
