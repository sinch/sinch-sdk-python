from typing import Optional
from pydantic import Field, StrictStr, conlist
from sinch.domains.numbers.models.v1.types import CapabilityType, NumberType
from sinch.domains.numbers.models.v1.internal.sms_configuration_request import (
    SmsConfigurationRequest,
)
from sinch.domains.numbers.models.v1.internal.voice_configuration_request import (
    VoiceConfigurationRequestUnion,
)
from sinch.domains.numbers.models.v1.shared.number_pattern import NumberPattern
from sinch.domains.numbers.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class RentAnyNumberRequest(BaseModelConfigurationRequest):
    region_code: StrictStr = Field(
        alias="regionCode",
        description="ISO 3166-1 alpha-2 country code. Example: US, GB or SE.",
    )
    number_type: NumberType = Field(alias="type")
    number_pattern: Optional[NumberPattern] = Field(
        default=None, alias="numberPattern"
    )
    capabilities: Optional[conlist(CapabilityType)] = Field(default=None)
    sms_configuration: Optional[SmsConfigurationRequest] = Field(
        default=None, alias="smsConfiguration"
    )
    voice_configuration: Optional[VoiceConfigurationRequestUnion] = Field(
        default=None, alias="voiceConfiguration"
    )
    event_destination_target: Optional[StrictStr] = Field(
        default=None, alias="callbackUrl"
    )
