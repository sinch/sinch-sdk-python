from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.voice.models import Price


@dataclass
class GetVoiceCallResponse(SinchBaseModel):
    from_: str
    to: dict
    domain: str
    call_id: str
    duration: int
    status: str
    result: str
    reason: str
    timestamp: str
    custom: dict
    user_rate: Price
    debit: Price


@dataclass
class UpdateVoiceCallResponse(SinchBaseModel):
    pass


class ManageVoiceCallResponse(SinchBaseModel):
    pass
