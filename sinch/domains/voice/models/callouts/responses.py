from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel


@dataclass
class CalloutResponse(SinchBaseModel):
    call_id: str
