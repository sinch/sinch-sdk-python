from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel


@dataclass
class SendConversationEventResponse(SinchBaseModel):
    accepted_time: str
    event_id: str
