from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class GetVoiceConferenceRequest(SinchRequestBaseModel):
    conference_id: str


@dataclass
class KickAllVoiceConferenceRequest(SinchRequestBaseModel):
    conference_id: str


@dataclass
class ManageParticipantVoiceConferenceRequest(SinchRequestBaseModel):
    conference_id: str
    call_id: str
    command: str
    moh: str


@dataclass
class KickParticipantVoiceConferenceRequest(SinchRequestBaseModel):
    conference_id: str
    call_id: str
