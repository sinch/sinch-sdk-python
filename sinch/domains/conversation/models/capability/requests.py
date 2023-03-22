from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class QueryConversationCapabilityRequest(SinchRequestBaseModel):
    app_id: str
    recipient: dict
    request_id: str
