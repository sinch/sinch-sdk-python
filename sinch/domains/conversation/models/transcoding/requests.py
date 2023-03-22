from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class TranscodeConversationMessageRequest(SinchRequestBaseModel):
    app_id: str
    app_message: dict
    channels: list
    from_: str
    to: str
