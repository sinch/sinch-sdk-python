from typing import Optional, Dict
from pydantic import Field, StrictStr
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationRequest
from sinch.domains.numbers.models.v1.utils.validators import validate_sms_voice_configuration


class UpdateNumberConfigurationRequest(BaseModelConfigurationRequest):
    phone_number: StrictStr = Field(alias="phoneNumber")
    display_name: Optional[StrictStr] = Field(default=None, alias="displayName")
    sms_configuration: Optional[Dict] = Field(default=None, alias="smsConfiguration")
    voice_configuration: Optional[Dict] = Field(default=None, alias="voiceConfiguration")
    callback_url: Optional[StrictStr] = Field(default=None, alias="callbackUrl")

    def __init__(self, **data):
        """
        Custom initializer to validate nested dictionaries.
        """
        if data.get("sms_configuration") or data.get("voice_configuration"):
            validate_sms_voice_configuration(data)
        super().__init__(**data)
