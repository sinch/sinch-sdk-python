from typing import Optional
from pydantic import Field, conlist
from sinch.domains.conversation.models.v1.messages.response.shared.card_message import (
    CardMessage,
)
from sinch.domains.conversation.models.v1.messages.response.types.choice_option import (
    ChoiceOption,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class CarouselMessage(BaseModelConfigurationResponse):
    cards: conlist(CardMessage) = Field(
        default=..., description="A list of up to 10 cards."
    )
    choices: Optional[conlist(ChoiceOption)] = Field(
        default=None,
        description="Optional. Outer choices on the carousel level. The number of outer choices is limited to 3.",
    )
