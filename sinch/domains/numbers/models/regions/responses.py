from dataclasses import dataclass
from typing import List

from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.numbers.models.regions import Region


@dataclass
class ListAvailableRegionsResponse(SinchBaseModel):
    available_regions: List[Region]
