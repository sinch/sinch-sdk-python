from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.numbers.models.v1.internal.sms_configuration_request import (
    SmsConfigurationRequest,
)
from sinch.domains.numbers.models.v1.internal.voice_configuration_request import (
    VoiceConfigurationRequestUnion,
)
from sinch.domains.numbers.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class RentNumberRequest(BaseModelConfigurationRequest):
    phone_number: StrictStr = Field(
        alias="phoneNumber",
        description="Phone number in E.164 format with leading '+'. Example: '+12025550134'.",
    )
    sms_configuration: Optional[SmsConfigurationRequest] = Field(
        default=None, alias="smsConfiguration"
    )
    voice_configuration: Optional[VoiceConfigurationRequestUnion] = Field(
        default=None, alias="voiceConfiguration"
    )
    event_destination_target: Optional[StrictStr] = Field(
        default=None, alias="callbackUrl"
    )
