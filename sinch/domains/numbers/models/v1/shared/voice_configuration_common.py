from datetime import datetime
from typing import Optional

from pydantic import Field

from sinch.domains.numbers.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.numbers.models.v1.shared.scheduled_voice_provisioning import (
    ScheduledVoiceProvisioning,
)


class VoiceConfigurationCommon(BaseModelConfigurationResponse):
    last_updated_time: Optional[datetime] = Field(
        default=None, alias="lastUpdatedTime"
    )
    scheduled_voice_provisioning: Optional[ScheduledVoiceProvisioning] = Field(
        default=None, alias="scheduledVoiceProvisioning"
    )
