from datetime import datetime
from typing import Literal, Optional, Union
from pydantic import Field, StrictStr
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationResponse
from sinch.domains.numbers.models.v1.types import ScheduledVoiceProvisioning


class VoiceConfigurationCommon(BaseModelConfigurationResponse):
    type: Optional[Union[Literal["RTC", "EST", "FAX"], StrictStr]]
    last_updated_time: Optional[datetime] = Field(default=None, alias="lastUpdatedTime")
    scheduled_voice_provisioning: Optional[ScheduledVoiceProvisioning] = Field(
        default=None, alias="scheduledVoiceProvisioning"
    )
