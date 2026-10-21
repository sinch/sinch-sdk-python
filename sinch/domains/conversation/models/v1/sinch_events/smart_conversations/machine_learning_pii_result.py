from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent


class MachineLearningPIIResult(SinchEvent):
    """An object that contains the PII analysis of the corresponding messages."""

    message: Optional[StrictStr] = Field(
        default=None, description="The message text that was analyzed."
    )
    masked: Optional[StrictStr] = Field(
        default=None,
        description="The redacted message text in which sensitive information was replaced with appropriate masks. A MISC mask is applied to a term that has been identified as PII, but with low confidence regarding which type of mask to assign.",
    )
