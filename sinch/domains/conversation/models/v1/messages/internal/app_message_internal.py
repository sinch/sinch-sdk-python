from typing import Optional, Union
from sinch.domains.conversation.models.v1.messages.shared.media_properties_internal import (
    MediaPropertiesInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.card_message_internal import (
    CardMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.types.carousel_message_internal import (
    CarouselMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.types.choice_message_internal import (
    ChoiceMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.types.list_message_internal import (
    ListMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.types.location_message_internal import (
    LocationMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.types.template_message_internal import (
    TemplateMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.conversation.models.v1.messages.shared.text_message_internal import (
    TextMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.types.contact_info_message_internal import (
    ContactInfoMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.app_message_common_props import (
    AppMessageCommonProps,
)


class CardAppMessageInternal(
    AppMessageCommonProps, BaseModelConfigurationResponse
):
    card_message: Optional[CardMessageInternal] = None


class CarouselAppMessageInternal(
    AppMessageCommonProps, BaseModelConfigurationResponse
):
    carousel_message: Optional[CarouselMessageInternal] = None


class ChoiceAppMessageInternal(
    AppMessageCommonProps, BaseModelConfigurationResponse
):
    choice_message: Optional[ChoiceMessageInternal] = None


class LocationAppMessageInternal(
    AppMessageCommonProps, BaseModelConfigurationResponse
):
    location_message: Optional[LocationMessageInternal] = None


class MediaAppMessageInternal(
    AppMessageCommonProps, BaseModelConfigurationResponse
):
    media_message: Optional[MediaPropertiesInternal] = None


class TemplateAppMessageInternal(
    AppMessageCommonProps, BaseModelConfigurationResponse
):
    template_message: Optional[TemplateMessageInternal] = None


class TextAppMessageInternal(
    AppMessageCommonProps, BaseModelConfigurationResponse
):
    text_message: Optional[TextMessageInternal] = None


class ListAppMessageInternal(
    AppMessageCommonProps, BaseModelConfigurationResponse
):
    list_message: Optional[ListMessageInternal] = None


class ContactInfoAppMessageInternal(
    AppMessageCommonProps, BaseModelConfigurationResponse
):
    contact_info_message: Optional[ContactInfoMessageInternal] = None


AppMessageInternal = Union[
    CardAppMessageInternal,
    CarouselAppMessageInternal,
    ChoiceAppMessageInternal,
    LocationAppMessageInternal,
    MediaAppMessageInternal,
    TemplateAppMessageInternal,
    TextAppMessageInternal,
    ListAppMessageInternal,
    ContactInfoAppMessageInternal,
]
