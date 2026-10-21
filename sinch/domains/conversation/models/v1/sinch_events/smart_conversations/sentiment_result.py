from typing import Optional, Union

from pydantic import Field, StrictFloat, StrictInt

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.sentiment_type import (
    SentimentType,
)


class SentimentResult(SinchEvent):
    sentiment: Optional[SentimentType] = Field(
        default=None,
        description="The most probable sentiment of the analyzed text.",
    )
    score: Optional[Union[StrictFloat, StrictInt]] = Field(
        default=None,
        description="The likelihood that the assigned sentiment represents the emotional context of the analyzed text. 1 is the maximum value, representing the highest likelihood that the message text matches the sentiment, and 0 is the minimum value, representing the lowest likelihood that the message text matches the sentiment.",
    )
