from dataclasses import dataclass

from sinch.core.models.base_model import SinchRequestBaseModel
from sinch.core.models.pagination import TokenPaginatedRequest


@dataclass
class ListActiveNumbersRequest(TokenPaginatedRequest):
    region_code: str
    number_type: str
    page_size: int
    capabilities: list
    number_search_pattern: str
    number_pattern: str


@dataclass
class GetNumberConfigurationRequest(SinchRequestBaseModel):
    phone_number: str


@dataclass
class UpdateNumberConfigurationRequest(SinchRequestBaseModel):
    phone_number: str
    display_name: str
    sms_configuration: dict
    voice_configuration: dict
    app_id: str


@dataclass
class ReleaseNumberFromProjectRequest(SinchRequestBaseModel):
    phone_number: str
