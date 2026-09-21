from typing import Literal, Optional
from pydantic import StrictStr, Field
from sinch.domains.numbers.models.v1.shared.scheduled_voice_provisioning_common import (
    ScheduledVoiceProvisioningCommon,
)


class ScheduledVoiceProvisioningEST(ScheduledVoiceProvisioningCommon):
    trunk_id: Optional[StrictStr] = Field(default=None, alias="trunkId")
    type: Literal["EST"] = Field(default="EST", alias="type")
