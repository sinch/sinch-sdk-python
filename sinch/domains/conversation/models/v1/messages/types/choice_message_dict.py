from typing import List, TypedDict
from typing_extensions import NotRequired

from sinch.domains.conversation.models.v1.messages.types.choice_option_dict import (
    ChoiceOptionDict,
)
from sinch.domains.conversation.models.v1.messages.types.message_properties_dict import (
    MessagePropertiesDict,
)
from sinch.domains.conversation.models.v1.messages.types.text_message_dict import (
    TextMessageDict,
)


class ChoiceMessageDict(TypedDict):
    choices: List[ChoiceOptionDict]
    text_message: NotRequired[TextMessageDict]
    message_properties: NotRequired[MessagePropertiesDict]
