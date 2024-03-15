from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class GetVoiceCallRequest(SinchRequestBaseModel):
    call_id: str


@dataclass
class UpdateVoiceCallRequest(SinchRequestBaseModel):
    call_id: str
    instructions: list
    action: dict


@dataclass
class ManageVoiceCallRequest(SinchRequestBaseModel):
    call_id: str
    call_leg: str
    instructions: list
    action: dict
