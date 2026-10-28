from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.document_field_classification import (
    DocumentFieldClassification,
)
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.document_image_classification import (
    DocumentImageClassification,
)
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.optical_character_recognition import (
    OpticalCharacterRecognition,
)


class MachineLearningImageRecognitionResult(SinchEvent):
    url: Optional[StrictStr] = Field(
        default=None, description="The URL of the image that was processed."
    )
    document_image_classification: Optional[DocumentImageClassification] = (
        Field(default=None)
    )
    optical_character_recognition: Optional[OpticalCharacterRecognition] = (
        Field(default=None)
    )
    document_field_classification: Optional[DocumentFieldClassification] = (
        Field(default=None)
    )
