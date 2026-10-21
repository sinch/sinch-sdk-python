from typing import Literal, Optional, Union

from pydantic import Field, StrictFloat, StrictInt, StrictStr

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent


class OffensiveAnalysis(SinchEvent):
    message: Optional[StrictStr] = Field(
        default=None,
        description="Either the message text or the URL of the image that was analyzed.",
    )
    url: Optional[StrictStr] = Field(
        default=None, description="URL of the image that was analyzed."
    )
    evaluation: Optional[Union[Literal["SAFE", "UNSAFE"], StrictStr]] = Field(
        default=None,
        description="A label, either SAFE or UNSAFE, that classifies the analyzed content.",
    )
    score: Optional[Union[StrictFloat, StrictInt]] = Field(
        default=None,
        description="The likelihood that the assigned evaluation represents the analyzed message correctly. 1 is the maximum value, representing the highest likelihood that the content of the message matches the evaluation. 0 is the minimum value, representing the lowest likelihood that the content of the message matches the evaluation.",
    )
