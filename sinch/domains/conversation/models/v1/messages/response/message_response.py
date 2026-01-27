from sinch.domains.conversation.models.v1.messages.shared import (
    MessageCommonProps,
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


class AppMessageResponse(MessageCommonProps, BaseModelConfiguration):
    app_message: AppMessage


class ContactMessageResponse(MessageCommonProps, BaseModelConfiguration):
    contact_message: ContactMessage
