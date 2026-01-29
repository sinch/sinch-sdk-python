from typing import List, Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.messages.types.conversation_channel_type import (
    ConversationChannelType,
)


class ChannelRecipientIdentity(BaseModelConfiguration):
    channel: ConversationChannelType = Field(
        ..., description="The conversation channel."
    )
    identity: StrictStr = Field(
        ..., description="The channel recipient identity."
    )


class IdentifiedBy(BaseModelConfiguration):
    channel_identities: List[ChannelRecipientIdentity] = Field(
        ...,
        description=(
            "A list of specific channel identities. "
            "The API will use these identities when sending to specific channels."
        ),
    )


class Recipient(BaseModelConfiguration):
    identified_by: Optional[IdentifiedBy] = Field(
        default=None,
        description="The identity as specified by the channel. Required if using Dispatch Mode.",
    )
    contact_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the contact.",
    )
