from typing import Optional

from pydantic import Field, StrictStr, conlist

from sinch.domains.conversation.models.v1.contacts.types.contact_language_type import (
    ContactLanguageType,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.shared.channel_identity import (
    ChannelIdentity,
)
from sinch.domains.conversation.models.v1.types.conversation_channel_type import (
    ConversationChannelType,
)


class CreateContactRequest(BaseModelConfiguration):
    channel_identities: conlist(ChannelIdentity) = Field(
        description="List of channel identities. Array must contain at least one item."
    )
    language: ContactLanguageType = Field(
        description="The language of the contact."
    )
    channel_priority: Optional[conlist(ConversationChannelType)] = Field(
        default=None,
        description="List of channels defining the channel priority. The channel at the top of the list is tried first.",
    )
    display_name: Optional[StrictStr] = Field(
        default=None,
        description="The display name. A default 'Unknown' will be assigned if left empty.",
    )
    email: Optional[StrictStr] = Field(
        default=None, description="Email of the contact."
    )
    external_id: Optional[StrictStr] = Field(
        default=None, description="Contact identifier in an external system."
    )
    metadata: Optional[StrictStr] = Field(
        default=None,
        description="Metadata associated with the contact. Up to 1024 characters long.",
    )
