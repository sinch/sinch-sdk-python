from datetime import datetime
from typing import Optional
from pydantic import Field, StrictStr, StrictInt
from sinch.domains.numbers.models.v1.internal.base_model_config import BaseModelConfigResponse
from sinch.domains.numbers.models.v1.shared_params import (
    CapabilityTypeValuesList, Money, NumberTypeValues, SmsConfigurationResponse
)
from sinch.domains.numbers.models.v1.shared_params import VoiceConfigurationResponse


class RentAnyNumberResponse(BaseModelConfigResponse):
    phone_number: Optional[StrictStr] = Field(default=None, alias="phoneNumber")
    project_id: Optional[StrictStr] = Field(default=None, alias="projectId")
    region_code: Optional[StrictStr] = Field(default=None, alias="regionCode")
    type: Optional[NumberTypeValues] = Field(default=None)
    capabilities: Optional[CapabilityTypeValuesList] = Field(default=None)
    money: Optional[Money] = Field(default=None)
    payment_interval_months: Optional[StrictInt] = Field(default=None, alias="paymentIntervalMonths")
    next_charge_date: Optional[datetime] = Field(default=None, alias="nextChargeDate")
    expire_at: Optional[datetime] = Field(default=None, alias="expireAt")
    sms_configuration: Optional[SmsConfigurationResponse] = Field(default=None, alias="smsConfiguration")
    voice_configuration: Optional[VoiceConfigurationResponse] = Field(default=None, alias="voiceConfiguration")
    callback_url: Optional[StrictStr] = Field(default=None, alias="callbackUrl")
