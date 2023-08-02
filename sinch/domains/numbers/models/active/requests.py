from dataclasses import dataclass

from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class ListActiveNumbersRequest(SinchRequestBaseModel):
    region_code: str
    number_type: str
    page_size: int = None
    capabilities: list = None
    number_search_pattern: str = None
    number_pattern: str = None
    page_token: str = None


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
