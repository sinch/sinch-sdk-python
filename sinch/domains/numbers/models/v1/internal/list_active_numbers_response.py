from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, StrictStr, StrictInt
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigResponse
from sinch.domains.numbers.models.v1.shared import Money, SmsConfigurationResponse, VoiceConfigurationResponse
from sinch.domains.numbers.models.v1.types import CapabilityType, NumberType


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


class ListActiveNumbersResponse(BaseModel):
    active_numbers: Optional[List[ActiveNumber]] = Field(default=None, alias="activeNumbers")
    next_page_token: Optional[StrictStr] = Field(default=None, alias="nextPageToken")
    total_size: Optional[StrictInt] = Field(default=None, alias="totalSize")

    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow",
    )

    @property
    def content(self):
        """Returns the active numbers as part of the response object to be used in the pagination."""
        return self.active_numbers or []
