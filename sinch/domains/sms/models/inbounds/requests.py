from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class ListSMSInboundMessageRequest(SinchRequestBaseModel):
    start_date: str
    to: str
    end_date: str
    page_size: int
    page_size: int
    client_reference: str
    page: int = 0


@dataclass
class GetSMSInboundMessageRequest(SinchRequestBaseModel):
    inbound_id: str
