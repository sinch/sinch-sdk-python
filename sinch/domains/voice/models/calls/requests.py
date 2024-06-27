from typing import Union, List
from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel
from sinch.domains.voice.models.svaml.actions.actions import Action
from sinch.domains.voice.models.svaml.instructions.instructions import Instruction


@dataclass
class GetVoiceCallRequest(SinchRequestBaseModel):
    call_id: str


@dataclass
class UpdateVoiceCallRequest(SinchRequestBaseModel):
    call_id: str
    instructions: Union[list, List[Instruction]]
    action: Action


@dataclass
class ManageVoiceCallRequest(SinchRequestBaseModel):
    call_id: str
    call_leg: str
    instructions: Union[list, List[Instruction]]
    action: Action
