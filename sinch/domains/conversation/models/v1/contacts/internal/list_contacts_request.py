from typing import Optional

from pydantic import Field, StrictInt, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.types.conversation_channel_type import (
    ConversationChannelType,
)


class ListContactsRequest(BaseModelConfiguration):
    page_size: Optional[StrictInt] = Field(
        default=None,
        description="Optional. The maximum number of contacts to fetch. The default is 10 and the maximum is 20.",
    )
    page_token: Optional[StrictStr] = Field(
        default=None,
        description="Optional. Next page token previously returned if any.",
    )
    external_id: Optional[StrictStr] = Field(
        default=None,
        description="Optional. Contact identifier in an external system. If used, `channel` and `identity` query parameters can't be used.",
    )
    channel: Optional[ConversationChannelType] = Field(
        default=None,
        description="Optional. Specifies a channel, and must be set to one of the enum values. If set, the `identity` parameter must be set and `external_id` can't be used. Used in conjunction with `identity` to uniquely identify the specified channel identity.",
    )
    identity: Optional[StrictStr] = Field(
        default=None,
        description="Optional. If set, the `channel` parameter must be set and `external_id` can't be used. Used in conjunction with `channel` to uniquely identify the specified channel identity. This will differ from channel to channel. For example, a phone number for SMS, WhatsApp, and Viber Business.",
    )
