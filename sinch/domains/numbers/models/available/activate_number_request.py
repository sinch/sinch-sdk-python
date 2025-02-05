from typing import Optional, Dict
from pydantic import Field, StrictStr
from sinch.domains.numbers.models.base_model_numbers import BaseModelConfigRequest
from sinch.domains.numbers.models.numbers import (SmsConfigurationRequest, VoiceConfigurationFAX,
                                                  VoiceConfigurationEST, VoiceConfigurationRTC,
                                                  VoiceConfigurationCustom)


class ActivateNumberRequest(BaseModelConfigRequest):
    phone_number: StrictStr = Field(alias="phoneNumber")
    # Accepts only dictionary input, not Pydantic models
    sms_configuration: Optional[Dict] = Field(default=None, alias="smsConfiguration")
    voice_configuration: Optional[Dict] = Field(default=None, alias="voiceConfiguration")
    callback_url: Optional[StrictStr] = Field(default=None, alias="callbackUrl")

    def __init__(self, **data):
        """
        Custom initializer to validate nested dictionaries.
        """
        for key in ("smsConfiguration", "sms_configuration"):
            if key in data and data[key] is not None:
                SmsConfigurationRequest(**data[key])

        voice_config_map = {
            "RTC": VoiceConfigurationRTC,
            "EST": VoiceConfigurationEST,
            "FAX": VoiceConfigurationFAX,
        }

        for key in ("voiceConfiguration", "voice_configuration"):
            if key in data and data[key] is not None:
                # Address legacy requests
                voice_type = data[key].get("type") or "RTC"
                voice_config_class = voice_config_map.get(voice_type, VoiceConfigurationCustom)
                voice_config_class(**data[key])

        super().__init__(**data)
