from typing import Optional
from pydantic import StrictStr, Field
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationResponse
from sinch.domains.numbers.models.v1.shared import ScheduledSmsProvisioning


class SmsConfigurationResponse(BaseModelConfigurationResponse):
    service_plan_id: StrictStr = Field(alias="servicePlanId")
    campaign_id: Optional[StrictStr] = Field(default=None, alias="campaignId")
    scheduled_provisioning: Optional[ScheduledSmsProvisioning] = (
        Field(default=None, alias="scheduledProvisioning"))
