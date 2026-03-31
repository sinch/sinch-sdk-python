from typing import Optional
from pydantic import Field
from sinch.domains.numbers.models.v1.shared.scheduled_sms_provisioning import (
    ScheduledSmsProvisioning,
)
from sinch.domains.numbers.models.v1.shared.sms_configuration_base import (
    SmsConfigurationBase,
)


class SmsConfiguration(SmsConfigurationBase):
    scheduled_provisioning: Optional[ScheduledSmsProvisioning] = Field(
        default=None, alias="scheduledProvisioning"
    )
