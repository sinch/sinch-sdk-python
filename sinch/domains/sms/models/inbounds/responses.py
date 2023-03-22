from dataclasses import dataclass
from typing import List
from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.sms.models.inbounds import InboundMessage


@dataclass
class SinchListInboundMessagesResponse(SinchBaseModel):
    page: str
    page_size: str
    count: str
    inbounds: List[InboundMessage]


@dataclass
class GetInboundMessagesResponse(InboundMessage):
    pass
