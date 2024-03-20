from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel


@dataclass
class VoiceCalloutResponse(SinchBaseModel):
    call_id: str
