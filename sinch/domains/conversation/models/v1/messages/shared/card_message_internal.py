from typing import Optional
from pydantic import Field, StrictStr, conlist
from sinch.domains.conversation.models.v1.messages.types.card_height_type import (
    CardHeightType,
)
from sinch.domains.conversation.models.v1.messages.shared.media_properties_internal import (
    MediaPropertiesInternal,
)
from sinch.domains.conversation.models.v1.messages.types.choice_message_one_of_internal import (
    ChoiceMessageOneOfInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.message_properties_internal import (
    MessagePropertiesInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class CardMessageInternal(BaseModelConfigurationResponse):
    choices: Optional[conlist(ChoiceMessageOneOfInternal)] = Field(
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
    media_message: Optional[MediaPropertiesInternal] = Field(
        default=None, description="A message containing a media component."
    )
    message_properties: Optional[MessagePropertiesInternal] = None
