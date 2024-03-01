from typing import List
from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class AssignNumbersVoiceApplicationRequest(SinchRequestBaseModel):
    numbers: List[str]
    application_key: str
    capability: str


@dataclass
class UnassignNumbersVoiceApplicationRequest(SinchRequestBaseModel):
    number: str
    application_key: str
    capability: str


@dataclass
class QueryNumberVoiceApplicationRequest(SinchRequestBaseModel):
    number: str


@dataclass
class UpdateCallbackUrlsVoiceApplicationRequest(SinchRequestBaseModel):
    application_key: str
    primary: str
    fallback: str


@dataclass
class GetCallbackUrlsVoiceApplicationRequest(SinchRequestBaseModel):
    application_key: str
