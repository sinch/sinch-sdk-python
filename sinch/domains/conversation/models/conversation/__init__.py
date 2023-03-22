from dataclasses import dataclass

from sinch.core.models.base_model import SinchBaseModel


@dataclass
class Conversation(SinchBaseModel):
    id: str
    app_id: str
    contact_id: str
    last_received: str
    active_channel: str
    active: str
    metadata: str
    metadata_json: str
