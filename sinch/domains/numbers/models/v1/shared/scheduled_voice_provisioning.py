from datetime import datetime
from typing import Literal, Optional
from pydantic import Field
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationResponse
from sinch.domains.numbers.models.v1.types import StatusScheduledProvisioning


class ScheduledVoiceProvisioning(BaseModelConfigurationResponse):
    type: Literal["FAX", "EST", "RTC"]
    last_updated_time: Optional[datetime] = Field(default=None, alias="lastUpdatedTime")
    status: Optional[StatusScheduledProvisioning] = None
