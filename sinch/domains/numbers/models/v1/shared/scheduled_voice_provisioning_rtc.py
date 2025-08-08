from typing import Optional
from pydantic import StrictStr, Field
from sinch.domains.numbers.models.v1.shared.scheduled_voice_provisioning_common import ScheduledVoiceProvisioningCommon


class ScheduledVoiceProvisioningRTC(ScheduledVoiceProvisioningCommon):
    app_id: Optional[StrictStr] = Field(default=None, alias="appId")
