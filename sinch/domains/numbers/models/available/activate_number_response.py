from datetime import datetime
from typing import Optional
from pydantic import Field, StrictInt, StrictStr, conlist
from sinch.domains.numbers.models.numbers import Money, SmsConfiguration, VoiceConfiguration
from sinch.core.models.base_model import BaseModelConfigResponse


class ActivateNumberResponse(BaseModelConfigResponse):
    phone_number: Optional[StrictStr] = Field(default=None, alias="phoneNumber")
    project_id: Optional[StrictStr] = Field(default=None, alias="projectId")
    display_name: Optional[StrictStr] = Field(default=None, alias="displayName")
    region_code: Optional[StrictStr] = Field(default=None, alias="regionCode")
    type: Optional[StrictStr] = None
    capability: Optional[conlist(StrictStr, min_length=1)] = None
    money: Optional[Money] = None
    payment_interval_months: Optional[StrictInt] = Field(default=None, alias="paymentIntervalMonths")
    next_charge_date: Optional[datetime] = Field(default=None, alias="nextChargeDate")
    expire_at: Optional[datetime] = Field(default=None, alias="expireAt")
    sms_configuration: Optional[SmsConfiguration] = Field(default=None, alias="smsConfiguration")
    voice_configuration: Optional[VoiceConfiguration] = Field(default=None, alias="voiceConfiguration")
    callback_url: Optional[StrictStr] = Field(default=None, alias="callbackUrl")
