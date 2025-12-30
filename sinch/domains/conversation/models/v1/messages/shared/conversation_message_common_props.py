from typing import Optional
from datetime import datetime
from pydantic import Field, StrictBool, StrictStr
from sinch.domains.conversation.models.v1.messages.shared.channel_identity import (
    ChannelIdentity,
)
from sinch.domains.conversation.models.v1.messages.types.conversation_direction_type import (
    ConversationDirectionType,
)
from sinch.domains.conversation.models.v1.messages.types.processing_mode_type import (
    ProcessingModeType,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ConversationMessageCommonProps(BaseModelConfigurationResponse):
    accept_time: Optional[datetime] = Field(
        default=None,
        description="The time Conversation API processed the message.",
    )
    channel_identity: Optional[ChannelIdentity] = Field(
        default=None,
        description="A unique identity of message recipient on a particular channel. For example, the channel identity on SMS, WHATSAPP or VIBERBM is a MSISDN phone number.",
    )
    contact_id: Optional[StrictStr] = Field(
        default=None, description="The ID of the contact."
    )
    conversation_id: Optional[StrictStr] = Field(
        default=None, description="The ID of the conversation."
    )
    direction: Optional[ConversationDirectionType] = None
    id: Optional[StrictStr] = Field(
        default=None, description="The ID of the message."
    )
    metadata: Optional[StrictStr] = Field(
        default=None,
        description="Optional. Metadata associated with the contact. Up to 1024 characters long.",
    )
    injected: Optional[StrictBool] = Field(
        default=None, description="Flag for whether this message was injected."
    )
    sender_id: Optional[StrictStr] = Field(
        default=None,
        description="For Contact Messages (MO messages), the sender ID represents the recipient to which the message was sent. This may be a phone number (in the case of SMS and MMS) or a unique ID (in the case of WhatsApp). This is field is not supported on all channels, nor is it supported for MT messages.",
    )
    processing_mode: Optional[ProcessingModeType] = Field(
        default=None,
        description="Whether or not Conversation API should store contacts and conversations for the app. For more information, see [Processing Modes](https://developers.sinch.com/docs/conversation/processing-modes/).",
    )
