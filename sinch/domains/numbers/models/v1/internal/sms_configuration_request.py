from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.numbers.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class SmsConfigurationRequest(BaseModelConfigurationRequest):
    service_plan_id: StrictStr = Field(alias="servicePlanId")
    campaign_id: Optional[StrictStr] = Field(default=None, alias="campaignId")
