from typing import Optional
from sinch.domains.conversation.models.v1.messages.categories.card.card_message import (
    CardMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.carousel.carousel_message import (
    CarouselMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.choice.choice_message import (
    ChoiceMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.contactinfo.contact_info_message import (
    ContactInfoMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.list.list_message import (
    ListMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.location.location_message import (
    LocationMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.media.media_properties import (
    MediaProperties,
)
from sinch.domains.conversation.models.v1.messages.categories.template.template_message import (
    TemplateMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.text import (
    TextMessage,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.messages.shared.app_message_common_props import (
    AppMessageCommonProps,
)


class CardAppMessage(AppMessageCommonProps, BaseModelConfiguration):
    card_message: Optional[CardMessage] = None


class CarouselAppMessage(AppMessageCommonProps, BaseModelConfiguration):
    carousel_message: Optional[CarouselMessage] = None


class ChoiceAppMessage(AppMessageCommonProps, BaseModelConfiguration):
    choice_message: Optional[ChoiceMessage] = None


class LocationAppMessage(AppMessageCommonProps, BaseModelConfiguration):
    location_message: Optional[LocationMessage] = None


class MediaAppMessage(AppMessageCommonProps, BaseModelConfiguration):
    media_message: Optional[MediaProperties] = None


class TemplateAppMessage(AppMessageCommonProps, BaseModelConfiguration):
    template_message: Optional[TemplateMessage] = None


class TextAppMessage(AppMessageCommonProps, BaseModelConfiguration):
    text_message: Optional[TextMessage] = None


class ListAppMessage(AppMessageCommonProps, BaseModelConfiguration):
    list_message: Optional[ListMessage] = None


class ContactInfoAppMessage(AppMessageCommonProps, BaseModelConfiguration):
    contact_info_message: Optional[ContactInfoMessage] = None
