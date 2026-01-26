from sinch.domains.conversation.models.v1.messages.shared import (
    MessageResponseCommonProps,
)
from sinch.domains.conversation.models.v1.messages.response.types.app_message import (
    AppMessage,
)
from sinch.domains.conversation.models.v1.messages.response.types.contact_message import (
    ContactMessage,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class AppMessageResponse(MessageResponseCommonProps, BaseModelConfiguration):
    app_message: AppMessage


class ContactMessageResponse(
    MessageResponseCommonProps, BaseModelConfiguration
):
    contact_message: ContactMessage
