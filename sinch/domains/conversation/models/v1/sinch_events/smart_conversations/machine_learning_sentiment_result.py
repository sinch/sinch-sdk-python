from typing import Optional

from pydantic import Field, StrictStr, conlist

from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.sentiment_result import (
    SentimentResult,
)


class MachineLearningSentimentResult(SentimentResult):
    message: Optional[StrictStr] = Field(
        default=None, description="The message text that was analyzed."
    )
    results: Optional[conlist(SentimentResult)] = Field(
        default=None,
        description="An array of JSON objects made up of sentiment and score pairs, where the score represents the likelihood that the message communicates the corresponding sentiment.",
    )
