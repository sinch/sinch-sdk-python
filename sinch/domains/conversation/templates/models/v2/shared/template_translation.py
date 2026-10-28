from typing import Annotated, Union

from pydantic import Field

from sinch.core.models.internal.unions import ResolveUnion
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
from sinch.domains.conversation.models.v1.messages.categories.text.text_message import (
    TextMessage,
)
from sinch.domains.conversation.templates.models.v2.shared.template_translation_base import (
    TemplateTranslationBase,
)


class TemplateTranslationCardMessage(TemplateTranslationBase):
    card_message: CardMessage = Field(default=...)


class TemplateTranslationCarouselMessage(TemplateTranslationBase):
    carousel_message: CarouselMessage = Field(default=...)


class TemplateTranslationChoiceMessage(TemplateTranslationBase):
    choice_message: ChoiceMessage = Field(default=...)


class TemplateTranslationLocationMessage(TemplateTranslationBase):
    location_message: LocationMessage = Field(default=...)


class TemplateTranslationMediaMessage(TemplateTranslationBase):
    media_message: MediaProperties = Field(default=...)


class TemplateTranslationTemplateMessage(TemplateTranslationBase):
    template_message: TemplateMessage = Field(default=...)


class TemplateTranslationTextMessage(TemplateTranslationBase):
    text_message: TextMessage = Field(default=...)


class TemplateTranslationListMessage(TemplateTranslationBase):
    list_message: ListMessage = Field(default=...)


class TemplateTranslationContactInfoMessage(TemplateTranslationBase):
    contact_info_message: ContactInfoMessage = Field(default=...)


TemplateTranslation = Annotated[
    Union[
        TemplateTranslationCardMessage,
        TemplateTranslationCarouselMessage,
        TemplateTranslationChoiceMessage,
        TemplateTranslationLocationMessage,
        TemplateTranslationMediaMessage,
        TemplateTranslationTemplateMessage,
        TemplateTranslationTextMessage,
        TemplateTranslationListMessage,
        TemplateTranslationContactInfoMessage,
    ],
    ResolveUnion(),
]
