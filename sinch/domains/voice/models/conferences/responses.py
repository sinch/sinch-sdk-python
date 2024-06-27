from dataclasses import dataclass
from typing import List
from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.voice.models import ConferenceParticipant


@dataclass
class GetVoiceConferenceResponse(SinchBaseModel):
    participants: List[ConferenceParticipant]


@dataclass
class KickAllVoiceConferenceResponse(SinchBaseModel):
    pass


@dataclass
class ManageParticipantVoiceConferenceResponse(SinchBaseModel):
    pass


@dataclass
class KickParticipantVoiceConferenceResponse(SinchBaseModel):
    pass
