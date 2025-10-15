from typing import Optional, Dict
from pydantic import Field, StrictStr
from sinch.domains.numbers.models.v1.utils.validators import (
    validate_sms_voice_configuration,
)
from sinch.domains.numbers.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class RentNumberRequest(BaseModelConfigurationRequest):
    phone_number: StrictStr = Field(alias="phoneNumber")
    # Accepts only dictionary input, not Pydantic models
    sms_configuration: Optional[Dict] = Field(
        default=None, alias="smsConfiguration"
    )
    voice_configuration: Optional[Dict] = Field(
        default=None, alias="voiceConfiguration"
    )
    callback_url: Optional[StrictStr] = Field(
        default=None, alias="callbackUrl"
    )

    def __init__(self, **data):
        """
        Custom initializer to validate nested dictionaries.
        """
        validate_sms_voice_configuration(data)
        super().__init__(**data)
