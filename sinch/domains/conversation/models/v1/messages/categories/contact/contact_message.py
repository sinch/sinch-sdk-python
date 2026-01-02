from typing import Optional
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.categories.choiceresponse import (
    ChoiceResponseMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.channel_specific_contact_message_message import (
    ChannelSpecificContactMessageMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.fallback import (
    FallbackMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.location.location_message import (
    LocationMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.media import (
    MediaProperties,
)
from sinch.domains.conversation.models.v1.messages.categories.mediacard import (
    MediaCardMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.productresponse import (
    ProductResponseMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.text import (
    TextMessage,
)
from sinch.domains.conversation.models.v1.messages.shared.contact_message_common_props import (
    ContactMessageCommonProps,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ChannelSpecificContactMessage(
    ContactMessageCommonProps, BaseModelConfigurationResponse
):
    channel_specific_message: ChannelSpecificContactMessageMessage = Field(
        ...,
        description="A contact message containing a channel specific message (not supported by OMNI types).",
    )


class ChoiceResponseContactMessage(
    ContactMessageCommonProps, BaseModelConfigurationResponse
):
    choice_response_message: Optional[ChoiceResponseMessage] = None


class FallbackContactMessage(
    ContactMessageCommonProps, BaseModelConfigurationResponse
):
    fallback_message: Optional[FallbackMessage] = None


class LocationContactMessage(
    ContactMessageCommonProps, BaseModelConfigurationResponse
):
    location_message: Optional[LocationMessage] = None


class MediaCardContactMessage(
    ContactMessageCommonProps, BaseModelConfigurationResponse
):
    media_card_message: Optional[MediaCardMessage] = None


class MediaContactMessage(
    ContactMessageCommonProps, BaseModelConfigurationResponse
):
    media_message: Optional[MediaProperties] = None


class ProductResponseContactMessage(
    ContactMessageCommonProps, BaseModelConfigurationResponse
):
    product_response_message: Optional[ProductResponseMessage] = None


class TextContactMessage(
    ContactMessageCommonProps, BaseModelConfigurationResponse
):
    text_message: Optional[TextMessage] = None
