from typing import List, TypedDict
from typing_extensions import NotRequired

from sinch.domains.conversation.models.v1.messages.types.card_message_dict import (
    CardMessageDict,
)
from sinch.domains.conversation.models.v1.messages.types.choice_option_dict import (
    ChoiceOptionDict,
)


class CarouselMessageDict(TypedDict):
    cards: List[CardMessageDict]
    choices: NotRequired[List[ChoiceOptionDict]]
