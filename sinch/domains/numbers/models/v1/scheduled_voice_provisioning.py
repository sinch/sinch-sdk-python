from datetime import datetime
from typing import Literal, Optional
from pydantic import Field
from sinch.domains.numbers.models.v1.internal import BaseModelConfigResponse
from sinch.domains.numbers.models.v1.status_scheduled_provisioning import StatusScheduledProvisioning


class ScheduledVoiceProvisioning(BaseModelConfigResponse):
    type: Literal["FAX", "EST", "RTC"]
    last_updated_time: Optional[datetime] = Field(default=None, alias="lastUpdatedTime")
    status: Optional[StatusScheduledProvisioning] = None
