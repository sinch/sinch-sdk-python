from typing import Optional
from pydantic import StrictStr, Field
from sinch.domains.numbers.models.v1.shared.scheduled_voice_provisioning_common import (
    ScheduledVoiceProvisioningCommon,
)


class ScheduledVoiceProvisioningFAX(ScheduledVoiceProvisioningCommon):
    service_id: Optional[StrictStr] = Field(default=None, alias="serviceId")
