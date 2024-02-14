from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class GetVoiceCallRequest(SinchRequestBaseModel):
    callId: str


@dataclass
class UpdateVoiceCallRequest(SinchRequestBaseModel):
    callId: str
    instructions: list
    action: dict
