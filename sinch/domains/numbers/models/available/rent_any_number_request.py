from typing import Optional, Union, Dict, Any
from pydantic import Field, StrictStr
from sinch.domains.numbers.models.base_model_numbers import BaseModelConfigRequest
from sinch.domains.numbers.models.numbers import (NumberSearchPatternType, CapabilityType,
                                                  SmsConfigurationRequest, VoiceConfigurationType)


class NumberPattern(BaseModelConfigRequest):
    pattern: Optional[StrictStr]
    search_pattern: Optional[NumberSearchPatternType] = Field(alias="searchPattern")


class RentAnyNumberRequest(BaseModelConfigRequest):
    region_code: StrictStr = Field(default=None, alias="regionCode")
    type_: StrictStr = Field(default=None, alias="type")
    number_pattern: Optional[NumberPattern] = Field(default=None, alias="numberPattern")
    capabilities: Optional[CapabilityType] = Field(default=None)
    sms_configuration: Optional[SmsConfigurationRequest] = Field(default=None, alias="smsConfiguration")
    voice_configuration: Union[VoiceConfigurationType, Dict[str, Any], None] = (
        Field(default=None, alias="voiceConfiguration"))
    callback_url: Optional[StrictStr] = Field(default=None, alias="callbackUrl")
