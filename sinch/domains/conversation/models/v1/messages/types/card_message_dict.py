from typing import List, TypedDict
from typing_extensions import NotRequired

from sinch.domains.conversation.models.v1.messages.types.card_height_type import (
    CardHeightType,
)
from sinch.domains.conversation.models.v1.messages.types.choice_option_dict import (
    ChoiceOptionDict,
)
from sinch.domains.conversation.models.v1.messages.types.media_properties_dict import (
    MediaPropertiesDict,
)
from sinch.domains.conversation.models.v1.messages.types.message_properties_dict import (
    MessagePropertiesDict,
)


class CardMessageDict(TypedDict):
    choices: NotRequired[List[ChoiceOptionDict]]
    description: NotRequired[str]
    height: NotRequired[CardHeightType]
    title: NotRequired[str]
    media_message: NotRequired[MediaPropertiesDict]
    message_properties: NotRequired[MessagePropertiesDict]
