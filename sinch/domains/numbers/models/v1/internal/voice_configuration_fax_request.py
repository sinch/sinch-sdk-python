from typing import Optional, Literal
from pydantic import Field, StrictStr
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationRequest


class VoiceConfigurationFAX(BaseModelConfigurationRequest):
    type: Literal["FAX"] = "FAX"
    service_id: Optional[StrictStr] = Field(default=None, alias="serviceId")
