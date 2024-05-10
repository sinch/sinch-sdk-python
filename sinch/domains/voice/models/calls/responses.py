from datetime import datetime
from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.voice.models import Price, Destination


@dataclass
class GetVoiceCallResponse(SinchBaseModel):
    from_: Destination
    to: Destination
    domain: str
    call_id: str
    duration: int
    status: str
    result: str
    reason: str
    timestamp: datetime
    custom: str
    user_rate: Price
    debit: Price


@dataclass
class UpdateVoiceCallResponse(SinchBaseModel):
    pass


class ManageVoiceCallResponse(SinchBaseModel):
    pass
