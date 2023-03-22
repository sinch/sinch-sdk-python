from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel


@dataclass
class TranscodeConversationMessageResponse(SinchBaseModel):
    transcoded_message: dict
