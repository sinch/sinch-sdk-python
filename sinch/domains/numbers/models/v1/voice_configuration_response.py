from datetime import datetime
from typing import Literal, Optional, Union
from pydantic import Field, StrictStr
from sinch.domains.numbers.models.v1.internal import BaseModelConfigResponse
from sinch.domains.numbers.models.v1.scheduled_voice_provisioning_custom import ScheduledVoiceProvisioningCustom
from sinch.domains.numbers.models.v1.scheduled_voice_provisioning_est import ScheduledVoiceProvisioningEST
from sinch.domains.numbers.models.v1.scheduled_voice_provisioning_fax import ScheduledVoiceProvisioningFAX
from sinch.domains.numbers.models.v1.scheduled_voice_provisioning_rtc import ScheduledVoiceProvisioningRTC


class VoiceConfigurationResponse(BaseModelConfigResponse):
    type: Union[Literal["RTC", "EST", "FAX"], StrictStr]
    last_updated_time: Optional[datetime] = Field(default=None, alias="lastUpdatedTime")
    scheduled_voice_provisioning: Union[ScheduledVoiceProvisioningRTC,
                                        ScheduledVoiceProvisioningEST,
                                        ScheduledVoiceProvisioningFAX,
                                        ScheduledVoiceProvisioningCustom,
                                        None] = Field(
        default=None, alias="scheduledVoiceProvisioning"
    )
    app_id: Optional[StrictStr] = Field(default=None, alias="appId")
