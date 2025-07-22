from typing import Optional
from pydantic import StrictStr, Field
from sinch.domains.numbers.models.v1.shared import ScheduledVoiceProvisioningCommon


class ScheduledVoiceProvisioningEST(ScheduledVoiceProvisioningCommon):
    trunk_id: Optional[StrictStr] = Field(default=None, alias="trunkId")
