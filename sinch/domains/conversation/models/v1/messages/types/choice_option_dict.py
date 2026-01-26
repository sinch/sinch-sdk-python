from typing import Any, TypedDict
from typing_extensions import NotRequired

from sinch.domains.conversation.models.v1.messages.types.calendar_message_dict import (
    CalendarMessageDict,
)
from sinch.domains.conversation.models.v1.messages.types.call_message_dict import (
    CallMessageDict,
)
from sinch.domains.conversation.models.v1.messages.types.location_message_dict import (
    LocationMessageDict,
)
from sinch.domains.conversation.models.v1.messages.types.share_location_message_dict import (
    ShareLocationMessageDict,
)
from sinch.domains.conversation.models.v1.messages.types.text_message_dict import (
    TextMessageDict,
)
from sinch.domains.conversation.models.v1.messages.types.url_message_dict import (
    UrlMessageDict,
)


class ChoiceOptionDict(TypedDict):
    # Optional metadata returned back to you as postback
    postback_data: NotRequired[Any]

    # Exactly one of the following keys is expected per choice:
    call_message: NotRequired[CallMessageDict]
    location_message: NotRequired[LocationMessageDict]
    text_message: NotRequired[TextMessageDict]
    url_message: NotRequired[UrlMessageDict]
    calendar_message: NotRequired[CalendarMessageDict]
    share_location_message: NotRequired[ShareLocationMessageDict]
