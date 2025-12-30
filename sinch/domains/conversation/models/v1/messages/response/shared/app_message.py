from typing import Optional
from sinch.domains.conversation.models.v1.messages.response.shared.media_properties import (
    MediaProperties,
)
from sinch.domains.conversation.models.v1.messages.response.shared.card_message import (
    CardMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.carousel_message import (
    CarouselMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.choice_message import (
    ChoiceMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.list_message import (
    ListMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.location_message import (
    LocationMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.template_message import (
    TemplateMessage,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.conversation.models.v1.messages.response.shared.text_message import (
    TextMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.contact_info_message import (
    ContactInfoMessage,
)
from sinch.domains.conversation.models.v1.messages.shared.app_message_common_props import (
    AppMessageCommonProps,
)


class CardAppMessage(AppMessageCommonProps, BaseModelConfigurationResponse):
    card_message: Optional[CardMessage] = None


class CarouselAppMessage(
    AppMessageCommonProps, BaseModelConfigurationResponse
):
    carousel_message: Optional[CarouselMessage] = None


class ChoiceAppMessage(AppMessageCommonProps, BaseModelConfigurationResponse):
    choice_message: Optional[ChoiceMessage] = None


class LocationAppMessage(
    AppMessageCommonProps, BaseModelConfigurationResponse
):
    location_message: Optional[LocationMessage] = None


class MediaAppMessage(AppMessageCommonProps, BaseModelConfigurationResponse):
    media_message: Optional[MediaProperties] = None


class TemplateAppMessage(
    AppMessageCommonProps, BaseModelConfigurationResponse
):
    template_message: Optional[TemplateMessage] = None


class TextAppMessage(AppMessageCommonProps, BaseModelConfigurationResponse):
    text_message: Optional[TextMessage] = None


class ListAppMessage(AppMessageCommonProps, BaseModelConfigurationResponse):
    list_message: Optional[ListMessage] = None


class ContactInfoAppMessage(
    AppMessageCommonProps, BaseModelConfigurationResponse
):
    contact_info_message: Optional[ContactInfoMessage] = None
