from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.contacts.types.get_channel_profile_conversation_channel_type import (
    GetChannelProfileConversationChannelType,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.messages.internal.request.recipient import (
    Recipient,
)


class GetChannelProfileRequest(BaseModelConfiguration):
    app_id: StrictStr = Field(description="The ID of the app.")
    recipient: Recipient = Field(description="The recipient.")
    channel: GetChannelProfileConversationChannelType = Field(
        description="The channel. Must be one of the supported channels for this operation."
    )
