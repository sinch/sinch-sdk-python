from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel


@dataclass
class InboundMessage(SinchBaseModel):
    type: str
    id: str
    from_: str
    to: str
    body: str
    operator_id: str
    send_at: str
    received_at: str
    client_reference: str
