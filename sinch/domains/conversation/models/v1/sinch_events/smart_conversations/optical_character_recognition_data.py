from typing import Optional

from pydantic import Field, StrictStr, conlist

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent


class OpticalCharacterRecognitionData(SinchEvent):
    data: Optional[conlist(StrictStr)] = Field(
        default=None,
        description="The data array contains the string(s) identified in one section of an analyzed image.",
    )
