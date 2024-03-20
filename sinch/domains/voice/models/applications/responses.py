from typing import List

from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.voice.models import ApplicationNumber, Price


@dataclass
class GetNumbersVoiceApplicationResponse(SinchBaseModel):
    numbers: List[ApplicationNumber]


@dataclass
class AssignNumbersVoiceApplicationResponse(SinchBaseModel):
    pass


@dataclass
class UnassignNumbersVoiceApplicationResponse(SinchBaseModel):
    pass


@dataclass
class UpdateCallbackUrlsVoiceApplicationResponse(SinchBaseModel):
    pass


@dataclass
class GetCallbackUrlsVoiceApplicationResponse(SinchBaseModel):
    primary: str
    fallback: str


@dataclass
class QueryNumberVoiceApplicationResponse(SinchBaseModel):
    country_id: str
    number_type: str
    normalized_number: str
    restricted: bool
    rate: Price
