from dataclasses import dataclass
from typing import List

from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.numbers.models import Number


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
