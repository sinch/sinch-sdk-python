from typing import Optional

from pydantic import Field, conlist

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.optical_character_recognition_data import (
    OpticalCharacterRecognitionData,
)


class OpticalCharacterRecognition(SinchEvent):
    """An object containing a result array that reports the machine learning engine's character extraction results."""

    result: Optional[conlist(OpticalCharacterRecognitionData)] = Field(
        default=None, description="The result of the OCR process."
    )
