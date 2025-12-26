from typing import Optional
from pydantic import Field, conlist
from sinch.domains.conversation.models.v1.messages.types.choice_message_one_of_internal import (
    ChoiceMessageOneOfInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.conversation.models.v1.messages.shared.text_message_internal import (
    TextMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.message_properties_internal import (
    MessagePropertiesInternal,
)


class ChoiceMessageInternal(BaseModelConfigurationResponse):
    choices: conlist(ChoiceMessageOneOfInternal) = Field(
        default=..., description="The number of choices is limited to 10."
    )
    text_message: Optional[TextMessageInternal] = None
    message_properties: Optional[MessagePropertiesInternal] = None
