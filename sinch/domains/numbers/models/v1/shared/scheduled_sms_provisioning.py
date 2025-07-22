from datetime import datetime
from typing import Optional
from pydantic import StrictStr, Field, conlist
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationResponse
from sinch.domains.numbers.models.v1.types.status_scheduled_provisioning import StatusScheduledProvisioning
from sinch.domains.numbers.models.v1.types.sms_error_code import SmsErrorCode


class ScheduledSmsProvisioning(BaseModelConfigurationResponse):
    service_plan_id: Optional[StrictStr] = Field(default=None, alias="servicePlanId")
    campaign_id: Optional[StrictStr] = Field(default=None, alias="campaignId")
    status: Optional[StatusScheduledProvisioning] = None
    last_updated_time: Optional[datetime] = Field(default=None, alias="lastUpdatedTime")
    error_codes: Optional[conlist(SmsErrorCode)] = Field(default=None, alias="errorCodes")
