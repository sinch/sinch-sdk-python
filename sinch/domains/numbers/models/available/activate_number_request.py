from typing import Optional, Dict, Literal
from pydantic import Field, StrictStr
from sinch.core.models.base_model import BaseModelConfigRequest


class SmsConfiguration(BaseModelConfigRequest):
    service_plan_id: StrictStr = Field(alias="servicePlanId")
    campaign_id: Optional[StrictStr] = Field(default=None, alias="campaignId")


class VoiceConfiguration(BaseModelConfigRequest):
    type: Literal["RTC", "EST", "FAX"]
    app_id: Optional[StrictStr] = Field(default=None, alias="appId")


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
        if "smsConfiguration" in data:
            # Validate dictionary and ensure correct structure
            SmsConfiguration(**data["smsConfiguration"])

        if "voiceConfiguration" in data:
            VoiceConfiguration(**data["voiceConfiguration"])

        super().__init__(**data)
