from dataclasses import dataclass

from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class ListAvailableNumbersRequest(SinchRequestBaseModel):
    region_code: str
    number_type: str
    page_size: int = None
    capabilities: list = None
    number_search_pattern: str = None
    number_pattern: str = None


@dataclass
class ActivateNumberRequest(SinchRequestBaseModel):
    phone_number: str
    sms_configuration: dict
    voice_configuration: dict


@dataclass
class CheckNumberAvailabilityRequest(SinchRequestBaseModel):
    phone_number: str