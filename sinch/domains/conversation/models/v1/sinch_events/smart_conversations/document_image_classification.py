from typing import Optional, Union

from pydantic import Field, StrictFloat, StrictInt, StrictStr

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent


class DocumentImageClassification(SinchEvent):
    """An object that identifies a document type within the image, along with a confidence level for that document type."""

    doc_type: Optional[StrictStr] = Field(
        default=None,
        description="The document type that the analyzed image most likely contains.",
    )
    confidence: Optional[Union[StrictFloat, StrictInt]] = Field(
        default=None,
        description="The likelihood that the analyzed image contains the assigned document type. 1 is the maximum value, representing the highest likelihood that the analyzed image contains the assigned document type, and 0 is the minimum value, representing the lowest likelihood that the analyzed image contains the assigned document type.",
    )
