from dataclasses import dataclass
from typing import TypedDict
from sinch.core.models.base_model import SinchRequestBaseModel


class Action(TypedDict):
    name: str


@dataclass
class GetVoiceCallRequest(SinchRequestBaseModel):
    call_id: str


@dataclass
class UpdateVoiceCallRequest(SinchRequestBaseModel):
    call_id: str
    instructions: list
    action: Action


@dataclass
class ManageVoiceCallRequest(SinchRequestBaseModel):
    call_id: str
    call_leg: str
    instructions: list
    action: Action
