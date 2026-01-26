from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class SendMessageResponse(BaseModelConfiguration):
    """
    Response from sending a message.
    """

    message_id: StrictStr = Field(
        ...,
        description="The ID of the sent message.",
    )
