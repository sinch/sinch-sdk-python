from typing import Optional
from pydantic import Field, StrictStr, conlist
from sinch.domains.conversation.models.v1.messages.types.card_height_type import (
    CardHeightType,
)
from sinch.domains.conversation.models.v1.messages.categories.media import (
    MediaProperties,
)
from sinch.domains.conversation.models.v1.messages.response.types.choice_option import (
    ChoiceOption,
)
from sinch.domains.conversation.models.v1.messages.categories.common.message_properties import (
    MessageProperties,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class CardMessage(BaseModelConfigurationResponse):
    choices: Optional[conlist(ChoiceOption)] = Field(
        default=None,
        description="You may include choices in your Card Message. The number of choices is limited to 10.",
    )
    description: Optional[StrictStr] = Field(
        default=None,
        description="This is an optional description field that is displayed below the title on the card.",
    )
    height: Optional[CardHeightType] = None
    title: Optional[StrictStr] = Field(
        default=None, description="The title of the card message."
    )
    media_message: Optional[MediaProperties] = Field(
        default=None, description="A message containing a media component."
    )
    message_properties: Optional[MessageProperties] = None
