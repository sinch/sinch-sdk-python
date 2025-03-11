from datetime import datetime
from typing import Optional

from pydantic import StrictStr, Field, conlist

from sinch.domains.numbers.models.v1.internal import BaseModelConfigResponse
from sinch.domains.numbers.models.v1.status_scheduled_provisioning import StatusScheduledProvisioning


class ScheduledSmsProvisioning(BaseModelConfigResponse):
    service_plan_id: Optional[StrictStr] = Field(default=None, alias="servicePlanId")
    campaign_id: Optional[StrictStr] = Field(default=None, alias="campaignId")
    status: Optional[StatusScheduledProvisioning] = None
    last_updated_time: Optional[datetime] = Field(default=None, alias="lastUpdatedTime")
    error_codes: Optional[conlist(StrictStr, min_length=0)] = Field(default=None, alias="errorCodes")
