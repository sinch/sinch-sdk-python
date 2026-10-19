from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ConversationIdRequest(BaseModelConfiguration):
    conversation_id: StrictStr = Field(
        description="The unique ID of the conversation."
    )
