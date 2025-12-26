from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ChoiceResponseMessageInternal(BaseModelConfigurationResponse):
    message_id: StrictStr = Field(
        ..., description="The message id containing the choice."
    )
    postback_data: StrictStr = Field(
        ..., description="The postback_data defined in the selected choice."
    )
