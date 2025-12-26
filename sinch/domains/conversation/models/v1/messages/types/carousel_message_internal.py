from typing import Optional
from pydantic import Field, conlist
from sinch.domains.conversation.models.v1.messages.shared.card_message_internal import (
    CardMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.types.choice_message_one_of_internal import (
    ChoiceMessageOneOfInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class CarouselMessageInternal(BaseModelConfigurationResponse):
    cards: conlist(CardMessageInternal) = Field(
        default=..., description="A list of up to 10 cards."
    )
    choices: Optional[conlist(ChoiceMessageOneOfInternal)] = Field(
        default=None,
        description="Optional. Outer choices on the carousel level. The number of outer choices is limited to 3.",
    )
