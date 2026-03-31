from typing import TypedDict
from typing_extensions import NotRequired
from sinch.domains.conversation.models.v1.messages.types.card_message_dict import (
    CardMessageDict,
)
from sinch.domains.conversation.models.v1.messages.types.carousel_message_dict import (
    CarouselMessageDict,
)
from sinch.domains.conversation.models.v1.messages.types.choice_message_dict import (
    ChoiceMessageDict,
)
from sinch.domains.conversation.models.v1.messages.types.contact_info_message_dict import (
    ContactInfoMessageDict,
)
from sinch.domains.conversation.models.v1.messages.types.list_message_dict import (
    ListMessageDict,
)
from sinch.domains.conversation.models.v1.messages.types.location_message_dict import (
    LocationMessageDict,
)
from sinch.domains.conversation.models.v1.messages.types.media_properties_dict import (
    MediaPropertiesDict,
)
from sinch.domains.conversation.models.v1.messages.types.template_message_dict import (
    TemplateMessageDict,
)
from sinch.domains.conversation.models.v1.messages.types.text_message_dict import (
    TextMessageDict,
)


class SendMessageRequestBodyDict(TypedDict, total=False):
    """
    TypedDict for the message body in send message requests.
    At least one message type must be provided.
    """

    text_message: NotRequired[TextMessageDict]
    card_message: NotRequired[CardMessageDict]
    carousel_message: NotRequired[CarouselMessageDict]
    choice_message: NotRequired[ChoiceMessageDict]
    contact_info_message: NotRequired[ContactInfoMessageDict]
    list_message: NotRequired[ListMessageDict]
    location_message: NotRequired[LocationMessageDict]
    media_message: NotRequired[MediaPropertiesDict]
    template_message: NotRequired[TemplateMessageDict]
