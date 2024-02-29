from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class GetNumbersVoiceApplicationRequest(SinchRequestBaseModel):
    pass


@dataclass
class AssignNumbersVoiceApplicationRequest(SinchRequestBaseModel):
    pass


@dataclass
class UnassignNumbersVoiceApplicationRequest(SinchRequestBaseModel):
    number: str
    application_key: str
    capability: str


@dataclass
class QueryNumberVoiceApplicationRequest(SinchRequestBaseModel):
    number: str
