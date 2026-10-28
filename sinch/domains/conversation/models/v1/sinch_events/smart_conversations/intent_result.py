from typing import Optional, Union

from pydantic import Field, StrictFloat, StrictInt, StrictStr

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent


class IntentResult(SinchEvent):
    intent: Optional[StrictStr] = Field(
        default=None,
        description="The most probable intent of the analyzed text. For example, chitchat.greeting, chitchat.bye, chitchat.compliment, chitchat.how_are_you, or general.yes_or_agreed.",
    )
    score: Optional[Union[StrictFloat, StrictInt]] = Field(
        default=None,
        description="The likelihood that the assigned intent represents the purpose of the analyzed text. 1 is the maximum value, representing the highest likelihood that the message text matches the intent, and 0 is the minimum value, representing the lowest likelihood that the message text matches the intent.",
    )
