from datetime import datetime
from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.messages.response.types.app_message import (
    AppMessage,
)
from sinch.domains.conversation.models.v1.messages.response.types.contact_message import (
    ContactMessage,
)
from sinch.domains.conversation.models.v1.messages.types.conversation_direction_type import (
    ConversationDirectionType,
)
from sinch.domains.conversation.models.v1.shared.channel_identity import (
    ChannelIdentity,
)
from sinch.domains.conversation.models.v1.types.processing_mode_type import (
    ProcessingModeType,
)


class InjectMessageRequest(BaseModelConfiguration):
    conversation_id: StrictStr = Field(
        description="The ID of the conversation."
    )
    app_message: AppMessage = Field(
        default=None,
        description="A message originating from a Conversation API app",
    )
    contact_message: ContactMessage = Field(
        default=None, description="A message originating from a contact."
    )
    accept_time: datetime = Field(
        description="The processed time of the message in UTC timezone. Must be less than current_time and greater than (current_time - 30 days)"
    )
    channel_identity: ChannelIdentity
    contact_id: StrictStr = Field(
        description="The ID of the contact registered in the conversation provided."
    )
    direction: ConversationDirectionType
    sender_id: Optional[StrictStr] = Field(
        default=None,
        description="For Contact Messages (MO messages), the sender ID represents the recipient to which the message was sent. This may be a phone number (in the case of SMS and MMS) or a unique ID (in the case of WhatsApp). This is field is not supported on all channels, nor is it supported for MT messages.",
    )
    processing_mode: Optional[ProcessingModeType] = None
    metadata: Optional[StrictStr] = Field(
        default=None,
        description="Optional. Metadata associated with the contact. Up to 1024 characters long.",
    )
