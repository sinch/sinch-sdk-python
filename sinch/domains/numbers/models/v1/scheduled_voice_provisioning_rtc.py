from typing import Optional
from pydantic import StrictStr, Field
from sinch.domains.numbers.models.v1.scheduled_voice_provisioning import ScheduledVoiceProvisioning


class ScheduledVoiceProvisioningRTC(ScheduledVoiceProvisioning):
    app_id: Optional[StrictStr] = Field(default=None, alias="appId")
