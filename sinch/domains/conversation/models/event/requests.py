from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class SendConversationEventRequest(SinchRequestBaseModel):
    app_id: str
    recipient: dict
    event: dict
    callback_url: str
    channel_priority_order: str
    event_metadata: str
    queue: str
