from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel


@dataclass
class QueryConversationCapabilityResponse(SinchBaseModel):
    request_id: str
    app_id: str
    recipient: dict
