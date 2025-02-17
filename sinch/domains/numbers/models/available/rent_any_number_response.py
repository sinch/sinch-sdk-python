from datetime import datetime
from typing import Optional
from pydantic import Field, StrictStr, StrictInt
from sinch.domains.numbers.models.base_model_numbers import BaseModelConfigResponse
from sinch.domains.numbers.models.numbers import (CapabilityTypeValuesList, Money, NumberTypeValues,
                                                  SmsConfigurationResponse, VoiceConfigurationResponse)


class RentAnyNumberResponse(BaseModelConfigResponse):
    phone_number: Optional[StrictStr] = Field(default=None, alias="phoneNumber")
    project_id: Optional[StrictStr] = Field(default=None, alias="projectId")
    region_code: Optional[StrictStr] = Field(default=None, alias="regionCode")
    type: Optional[NumberTypeValues] = Field(default=None)
    capability: Optional[CapabilityTypeValuesList] = Field(default=None)
    money: Optional[Money] = Field(default=None)
    payment_interval_months: Optional[StrictInt] = Field(default=None, alias="paymentIntervalMonths")
    next_charge_date: Optional[datetime] = Field(default=None, alias="nextChargeDate")
    expire_at: Optional[datetime] = Field(default=None, alias="expireAt")
    sms_configuration: Optional[SmsConfigurationResponse] = Field(default=None, alias="smsConfiguration")
    voice_configuration: Optional[VoiceConfigurationResponse] = Field(default=None, alias="voiceConfiguration")
    callback_url: Optional[StrictStr] = Field(default=None, alias="callbackUrl")
