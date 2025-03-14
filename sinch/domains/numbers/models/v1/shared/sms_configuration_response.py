from typing import Optional

from pydantic import StrictStr, Field

from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigResponse
from sinch.domains.numbers.models.v1.shared.scheduled_sms_provisioning import ScheduledSmsProvisioning


class SmsConfigurationResponse(BaseModelConfigResponse):
    service_plan_id: StrictStr = Field(alias="servicePlanId")
    campaign_id: Optional[StrictStr] = Field(default=None, alias="campaignId")
    scheduled_provisioning: Optional[ScheduledSmsProvisioning] = (
        Field(default=None, alias="scheduledProvisioning"))
