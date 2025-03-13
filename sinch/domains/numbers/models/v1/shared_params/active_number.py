from datetime import datetime
from typing import Optional
from pydantic import StrictStr, Field, StrictInt
from sinch.domains.numbers.models.v1.internal import BaseModelConfigResponse
from sinch.domains.numbers.models.v1.shared_params import (
    CapabilityType, Money, NumberType, SmsConfigurationResponse, VoiceConfigurationResponse
)


class ActiveNumber(BaseModelConfigResponse):
    phone_number: Optional[StrictStr] = Field(default=None, alias="phoneNumber")
    project_id: Optional[StrictStr] = Field(default=None, alias="projectId")
    display_name: Optional[StrictStr] = Field(default=None, alias="displayName")
    region_code: Optional[StrictStr] = Field(default=None, alias="regionCode")
    type: Optional[NumberType] = Field(default=None)
    capabilities: Optional[CapabilityType] = Field(default=None)
    money: Optional[Money] = Field(default=None)
    payment_interval_months: Optional[StrictInt] = Field(default=None, alias="paymentIntervalMonths")
    next_charge_date: Optional[datetime] = Field(default=None, alias="nextChargeDate")
    expire_at: Optional[datetime] = Field(default=None, alias="expireAt")
    sms_configuration: Optional[SmsConfigurationResponse] = Field(default=None, alias="smsConfiguration")
    voice_configuration: Optional[VoiceConfigurationResponse] = Field(default=None, alias="voiceConfiguration")
    callback_url: Optional[StrictStr] = Field(default=None, alias="callbackUrl")
