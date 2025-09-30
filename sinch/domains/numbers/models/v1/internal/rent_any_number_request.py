from typing import Optional, Dict, Any
from pydantic import Field, StrictStr, conlist
from sinch.domains.numbers.models.v1.types import CapabilityType, NumberType
from sinch.domains.numbers.models.v1.utils.validators import validate_sms_voice_configuration, validate_number_pattern
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationRequest


class RentAnyNumberRequest(BaseModelConfigurationRequest):
    region_code: StrictStr = Field(alias="regionCode")
    number_type: NumberType = Field(alias="type")
    number_pattern: Optional[Dict[str, Any]] = Field(default=None, alias="numberPattern")
    capabilities: Optional[conlist(CapabilityType)] = Field(default=None)
    sms_configuration: Optional[Dict[str, Any]] = Field(default=None, alias="smsConfiguration")
    voice_configuration: Optional[Dict[str, Any]] = Field(default=None, alias="voiceConfiguration")
    callback_url: Optional[StrictStr] = Field(default=None, alias="callbackUrl")

    def __init__(self, **data):
        """
        Custom initializer to validate nested dictionaries.
        """
        validate_sms_voice_configuration(data)
        validate_number_pattern(data)
        super().__init__(**data)
