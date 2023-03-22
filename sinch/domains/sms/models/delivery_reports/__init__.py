from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel


@dataclass
class DeliveryReport(SinchBaseModel):
    at: str
    batch_id: str
    code: int
    recipient: str
    status: str
    applied_originator: str
    client_reference: str
    encoding: str
    number_of_message_parts: int
    operator: str
    operator_status_at: str
    type: str
