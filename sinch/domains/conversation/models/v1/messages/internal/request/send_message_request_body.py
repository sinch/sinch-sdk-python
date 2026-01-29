from typing import Optional
from sinch.domains.conversation.models.v1.messages.categories.text import (
    TextMessage,
)
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
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class SendMessageRequestBody(BaseModelConfiguration):
    text_message: Optional[TextMessage] = None
    card_message: Optional[CardMessage] = None
    carousel_message: Optional[CarouselMessage] = None
    choice_message: Optional[ChoiceMessage] = None
    contact_info_message: Optional[ContactInfoMessage] = None
    list_message: Optional[ListMessage] = None
    location_message: Optional[LocationMessage] = None
    media_message: Optional[MediaProperties] = None
    template_message: Optional[TemplateMessage] = None
