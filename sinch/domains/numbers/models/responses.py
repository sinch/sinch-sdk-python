from typing import List, Optional
from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.numbers.models import Number, Region, ActiveNumber


@dataclass
class ListActiveNumbersResponse(SinchBaseModel):
    active_numbers: List[ActiveNumber]
    next_page_token: Optional[str] = None


@dataclass
class ListAvailableNumbersResponse(SinchBaseModel):
    available_numbers: List[Number]


@dataclass
class ActivateNumberResponse(SinchBaseModel):
    phone_number: str
    region_code: str
    type: str
    capability: tuple


@dataclass
class CheckNumberAvailabilityResponse(Number):
    pass


@dataclass
class UpdateNumberConfigurationResponse(ActiveNumber):
    pass


@dataclass
class GetNumberConfigurationResponse(ActiveNumber):
    pass


@dataclass
class ReleaseNumberFromProjectResponse(ActiveNumber):
    pass


@dataclass
class ListAvailableRegionsResponse(SinchBaseModel):
    available_regions: List[Region]
