from datetime import datetime
from typing import Optional
from pydantic import Field
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationResponse
from sinch.domains.numbers.models.v1.types.status_scheduled_provisioning import StatusScheduledProvisioning
from sinch.domains.numbers.models.v1.types.voice_application_type import VoiceApplicationType


class ScheduledVoiceProvisioningCommon(BaseModelConfigurationResponse):
    type: VoiceApplicationType
    last_updated_time: Optional[datetime] = Field(default=None, alias="lastUpdatedTime")
    status: Optional[StatusScheduledProvisioning] = None
