from typing import List, Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.messages.response.types.app_message import (
    AppMessage,
)
from sinch.domains.conversation.models.v1.types.conversation_channel_type import (
    ConversationChannelType,
)


class TranscodeMessageRequest(BaseModelConfiguration):
    app_id: StrictStr = Field(
        description="The ID of the app used to transcode the message."
    )
    app_message: AppMessage = Field(
        description="The message to be transcoded."
    )
    channels: List[ConversationChannelType] = Field(
        description="The list of channels for which the message shall be transcoded."
    )
    from_: Optional[StrictStr] = Field(
        default=None, alias="from", description="Optional."
    )
    to: Optional[StrictStr] = Field(default=None, description="Optional.")
