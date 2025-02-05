from typing import Optional, Dict
from pydantic import Field, StrictStr
from sinch.domains.numbers.validators import validate_sms_voice_configuration
from sinch.domains.numbers.models.base_model_numbers import BaseModelConfigRequest
from sinch.domains.numbers.models.numbers import NumberSearchPatternType, CapabilityType


class NumberPattern(BaseModelConfigRequest):
    pattern: Optional[StrictStr]
    search_pattern: Optional[NumberSearchPatternType] = Field(alias="searchPattern")


class RentAnyNumberRequest(BaseModelConfigRequest):
    region_code: StrictStr = Field(default=None, alias="regionCode")
    type_: StrictStr = Field(default=None, alias="type")
    number_pattern: Optional[NumberPattern] = Field(default=None, alias="numberPattern")
    capabilities: Optional[CapabilityType] = Field(default=None)
    sms_configuration: Optional[Dict] = Field(default=None, alias="smsConfiguration")
    voice_configuration: Optional[Dict] = Field(default=None, alias="voiceConfiguration")
    callback_url: Optional[StrictStr] = Field(default=None, alias="callbackUrl")

    def __init__(self, **data):
        """
        Custom initializer to validate nested dictionaries.
        """
        validate_sms_voice_configuration(data)
        super().__init__(**data)
