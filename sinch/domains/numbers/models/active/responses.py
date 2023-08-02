from dataclasses import dataclass
from typing import List, Optional

from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.numbers.models.active import ActiveNumber


@dataclass
class ListActiveNumbersResponse(SinchBaseModel):
    active_numbers: List[ActiveNumber]
    next_page_token: Optional[str] = None


@dataclass
class UpdateNumberConfigurationResponse(ActiveNumber):
    pass


@dataclass
class GetNumberConfigurationResponse(ActiveNumber):
    pass


@dataclass
class ReleaseNumberFromProjectResponse(ActiveNumber):
    pass