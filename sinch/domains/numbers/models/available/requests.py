from typing import Optional, Dict
from pydantic import Field, StrictStr, StrictInt, conlist
from sinch.core.models.base_model import BaseModelConfig


class ListAvailableNumbersRequest(BaseModelConfig):
    region_code: StrictStr = Field(alias="regionCode")
    number_type: StrictStr = Field(alias="type")
    page_size: Optional[StrictInt] = Field(default=None, alias="size")
    capabilities: Optional[conlist(StrictStr)] = None
    number_search_pattern: Optional[StrictStr] = Field(default=None, alias="numberPattern.searchPattern")
    number_pattern: Optional[StrictStr] = Field(default=None, alias="numberPattern.pattern")


class ActivateNumberRequest(BaseModelConfig):
    phone_number: str = Field(alias="phoneNumber")
    sms_configuration: Optional[Dict] = Field(default=None, alias="smsConfiguration")
    voice_configuration: Optional[Dict] = Field(default=None, alias="voiceConfiguration")
    callback_url: Optional[str] = Field(default=None, alias="callbackUrl")


class RentAnyNumberRequest(BaseModelConfig):
    region_code: Optional[str] = Field(default=None, alias="regionCode")
    type_: Optional[str] = Field(default=None, alias="type")
    number_pattern: Optional[Dict] = Field(default=None, alias="numberPattern")
    capabilities: Optional[list] = None
    sms_configuration: Optional[Dict] = Field(default=None, alias="smsConfiguration")
    voice_configuration: Optional[Dict] = Field(default=None, alias="voiceConfiguration")
    callback_url: Optional[str] = Field(default=None, alias="callbackUrl")


class CheckNumberAvailabilityRequest(BaseModelConfig):
    phone_number: str = Field(alias="phoneNumber")
