from dataclasses import dataclass

from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class ListAvailableNumbersRequest(SinchRequestBaseModel):
    region_code: str
    number_type: str
    page_size: int
    capabilities: list
    number_search_pattern: str
    number_pattern: str


@dataclass
class ActivateNumberRequest(SinchRequestBaseModel):
    phone_number: str
    sms_configuration: dict
    voice_configuration: dict


@dataclass
class RentAnyNumberRequest(SinchRequestBaseModel):
    region_code: str
    type_: str
    number_pattern: str
    capabilities: list
    sms_configuration: dict
    voice_configuration: dict
    callback_url: str


@dataclass
class CheckNumberAvailabilityRequest(SinchRequestBaseModel):
    phone_number: str
