from typing import Optional
from pydantic import StrictStr, Field
from sinch.domains.numbers.models.v1.shared import ScheduledVoiceProvisioning


class ScheduledVoiceProvisioningFAX(ScheduledVoiceProvisioning):
    service_id: Optional[StrictStr] = Field(default=None, alias="serviceId")
