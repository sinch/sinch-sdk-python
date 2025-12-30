from typing import Any, Optional
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.response.shared.call_message import (
    CallMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.location_message import (
    LocationMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.url_message import (
    UrlMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.calendar_message import (
    CalendarMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.share_location_message import (
    ShareLocationMessage,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.conversation.models.v1.messages.response.shared.text_message import (
    TextMessage,
)


class ChoiceMessageWithPostback(BaseModelConfigurationResponse):
    postback_data: Optional[Any] = Field(
        default=None,
        description="An optional field. This data will be returned in the ChoiceResponseMessage. The default is message_id_{text, title}.",
    )


class CallChoiceMessage(ChoiceMessageWithPostback):
    call_message: Optional[CallMessage] = None


class LocationChoiceMessage(ChoiceMessageWithPostback):
    location_message: Optional[LocationMessage] = None


class TextChoiceMessage(ChoiceMessageWithPostback):
    text_message: Optional[TextMessage] = None


class UrlChoiceMessage(ChoiceMessageWithPostback):
    url_message: Optional[UrlMessage] = None


class CalendarChoiceMessage(ChoiceMessageWithPostback):
    calendar_message: Optional[CalendarMessage] = None


class ShareLocationChoiceMessage(ChoiceMessageWithPostback):
    share_location_message: Optional[ShareLocationMessage] = None
