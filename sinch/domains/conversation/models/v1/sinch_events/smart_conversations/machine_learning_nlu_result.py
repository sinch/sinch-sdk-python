from typing import Optional

from pydantic import Field, StrictStr, conlist

from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.intent_result import (
    IntentResult,
)


class MachineLearningNLUResult(IntentResult):
    message: Optional[StrictStr] = Field(
        default=None, description="The message text that was analyzed."
    )
    results: Optional[conlist(IntentResult)] = Field(
        default=None,
        description="An array of JSON objects made up of intent and score pairs, where the score represents the likelihood that the message has the corresponding intent.",
    )
