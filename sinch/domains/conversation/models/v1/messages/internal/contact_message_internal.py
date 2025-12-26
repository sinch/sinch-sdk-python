from typing import Optional, Union
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.shared.media_properties_internal import (
    MediaPropertiesInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.contact_message_common_props import (
    ContactMessageCommonProps,
)
from sinch.domains.conversation.models.v1.messages.types.location_message_internal import (
    LocationMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.types.fallback_message_internal import (
    FallbackMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.types.media_card_message_internal import (
    MediaCardMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.types.product_response_message_internal import (
    ProductResponseMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.types.channel_specific_contact_message_message_internal import (
    ChannelSpecificContactMessageMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.choice_response_message_internal import (
    ChoiceResponseMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.text_message_internal import (
    TextMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ChannelSpecificContactMessageInternal(
    ContactMessageCommonProps, BaseModelConfigurationResponse
):
    channel_specific_message: ChannelSpecificContactMessageMessageInternal = Field(
        ...,
        description="A contact message containing a channel specific message (not supported by OMNI types).",
    )


class ChoiceResponseContactMessageInternal(
    ContactMessageCommonProps, BaseModelConfigurationResponse
):
    choice_response_message: Optional[ChoiceResponseMessageInternal] = None


class FallbackContactMessageInternal(
    ContactMessageCommonProps, BaseModelConfigurationResponse
):
    fallback_message: Optional[FallbackMessageInternal] = None


class LocationContactMessageInternal(
    ContactMessageCommonProps, BaseModelConfigurationResponse
):
    location_message: Optional[LocationMessageInternal] = None


class MediaCardContactMessageInternal(
    ContactMessageCommonProps, BaseModelConfigurationResponse
):
    media_card_message: Optional[MediaCardMessageInternal] = None


class MediaContactMessageInternal(
    ContactMessageCommonProps, BaseModelConfigurationResponse
):
    media_message: Optional[MediaPropertiesInternal] = None


class ProductResponseContactMessageInternal(
    ContactMessageCommonProps, BaseModelConfigurationResponse
):
    product_response_message: Optional[ProductResponseMessageInternal] = None


class TextContactMessageInternal(
    ContactMessageCommonProps, BaseModelConfigurationResponse
):
    text_message: Optional[TextMessageInternal] = None


ContactMessageInternal = Union[
    ChannelSpecificContactMessageInternal,
    ChoiceResponseContactMessageInternal,
    FallbackContactMessageInternal,
    LocationContactMessageInternal,
    MediaCardContactMessageInternal,
    MediaContactMessageInternal,
    ProductResponseContactMessageInternal,
    TextContactMessageInternal,
]
