from typing import Optional
from pydantic import Field, conlist
from sinch.domains.conversation.models.v1.messages.response.types.choice_option import (
    ChoiceOption,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.conversation.models.v1.messages.categories.text import (
    TextMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.common.message_properties import (
    MessageProperties,
)


class ChoiceMessage(BaseModelConfigurationResponse):
    choices: conlist(ChoiceOption) = Field(
        default=..., description="The number of choices is limited to 10."
    )
    text_message: Optional[TextMessage] = None
    message_properties: Optional[MessageProperties] = None
