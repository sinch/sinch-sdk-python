from typing import Optional, Dict
from pydantic import Field, StrictStr
from sinch.domains.numbers.models.v1.shared import NumberPattern
from sinch.domains.numbers.models.v1.types import CapabilityType
from sinch.domains.numbers.models.v1.utils.validators import validate_sms_voice_configuration
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationRequest


class RentAnyNumberRequest(BaseModelConfigurationRequest):
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
