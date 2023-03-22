from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel


@dataclass
class ConversationTemplate(SinchBaseModel):
    id: str
    description: str
    default_translation: str
    create_time: str
    translations: list
    update_time: str
    channel: str
