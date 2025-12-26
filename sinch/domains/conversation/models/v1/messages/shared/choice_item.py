from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.shared.media_properties_internal import (
    MediaPropertiesInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ChoiceItem(BaseModelConfigurationResponse):
    title: StrictStr = Field(
        default=...,
        description="Required parameter. Title for the choice item.",
    )
    description: Optional[StrictStr] = Field(
        default=None,
        description="Optional parameter. The description (or subtitle) of this choice item.",
    )
    media: Optional[MediaPropertiesInternal] = Field(
        default=None,
        description="Optional parameter. The media of this choice item.",
    )
    postback_data: Optional[StrictStr] = Field(
        default=None,
        description="Optional parameter. Postback data that will be returned in the MO if the user selects this option.",
    )
