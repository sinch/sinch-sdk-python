from typing import Optional

from pydantic import Field, StrictBool, StrictInt, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.types.conversation_channel_type import (
    ConversationChannelType,
)


class ListConversationsRequest(BaseModelConfiguration):
    app_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the app involved in the conversations.",
    )
    contact_id: Optional[StrictStr] = Field(
        default=None, description="Resource name (ID) of the contact."
    )
    only_active: Optional[StrictBool] = Field(
        default=None,
        description="Set to `true` to list only active conversations. Set to `false` to list only inactive conversations.",
    )
    page_size: Optional[StrictInt] = Field(
        default=None,
        description="The maximum number of conversations to fetch. Defaults to 10 and the maximum is 20.",
    )
    page_token: Optional[StrictStr] = Field(
        default=None, description="Next page token previously returned if any."
    )
    active_channel: Optional[ConversationChannelType] = Field(
        default=None,
        description="Only fetch conversations from the `active_channel`",
    )
