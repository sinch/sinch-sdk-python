from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel


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
    user_rate: dict
    debit: dict


@dataclass
class UpdateVoiceCallResponse(SinchBaseModel):
    pass
