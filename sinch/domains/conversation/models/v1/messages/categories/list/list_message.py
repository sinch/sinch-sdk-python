from typing import Optional
from pydantic import Field, StrictStr, conlist
from sinch.domains.conversation.models.v1.messages.shared.list_section import (
    ListSection,
)
from sinch.domains.conversation.models.v1.messages.categories.media import (
    MediaProperties,
)
from sinch.domains.conversation.models.v1.messages.categories.list.list_message_properties import (
    ListMessageProperties,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ListMessage(BaseModelConfigurationResponse):
    title: StrictStr = Field(
        default=...,
        description="A title for the message that is displayed near the products or choices.",
    )
    description: Optional[StrictStr] = Field(
        default=None,
        description="This is an optional field, containing a description for the message.",
    )
    media: Optional[MediaProperties] = None
    sections: conlist(ListSection) = Field(
        default=...,
        description="List of ListSection objects containing choices to be presented in the list message.",
    )
    message_properties: Optional[ListMessageProperties] = None
