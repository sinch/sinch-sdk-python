from typing import Any, Optional, Union
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.shared.call_message_internal import (
    CallMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.types.location_message_internal import (
    LocationMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.types.url_message_internal import (
    UrlMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.calendar_message_internal import (
    CalendarMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.share_location_message_internal import (
    ShareLocationMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.conversation.models.v1.messages.shared.text_message_internal import (
    TextMessageInternal,
)


class ChoiceMessageWithPostback(BaseModelConfigurationResponse):
    postback_data: Optional[Any] = Field(
        default=None,
        description="An optional field. This data will be returned in the ChoiceResponseMessage. The default is message_id_{text, title}.",
    )


class CallChoiceMessageInternal(ChoiceMessageWithPostback):
    call_message: Optional[CallMessageInternal] = None


class LocationChoiceMessageInternal(ChoiceMessageWithPostback):
    location_message: Optional[LocationMessageInternal] = None


class TextChoiceMessageInternal(ChoiceMessageWithPostback):
    text_message: Optional[TextMessageInternal] = None


class UrlChoiceMessageInternal(ChoiceMessageWithPostback):
    url_message: Optional[UrlMessageInternal] = None


class CalendarChoiceMessageInternal(ChoiceMessageWithPostback):
    calendar_message: Optional[CalendarMessageInternal] = None


class ShareLocationChoiceMessageInternal(ChoiceMessageWithPostback):
    share_location_message: Optional[ShareLocationMessageInternal] = None


ChoiceMessageOneOfInternal = Union[
    CallChoiceMessageInternal,
    LocationChoiceMessageInternal,
    TextChoiceMessageInternal,
    UrlChoiceMessageInternal,
    CalendarChoiceMessageInternal,
    ShareLocationChoiceMessageInternal,
]
