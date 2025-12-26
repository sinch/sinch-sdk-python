from typing import Union
from sinch.domains.conversation.models.v1.messages.shared import (
    ConversationMessageCommonProps,
)
from sinch.domains.conversation.models.v1.messages.internal.app_message_internal import (
    AppMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.contact_message_internal import (
    ContactMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class AppMessageConversationMessageInternal(
    ConversationMessageCommonProps, BaseModelConfigurationResponse
):
    app_message: AppMessageInternal


class ContactMessageConversationMessageInternal(
    ConversationMessageCommonProps, BaseModelConfigurationResponse
):
    contact_message: ContactMessageInternal


ConversationMessageResponse = Union[
    AppMessageConversationMessageInternal,
    ContactMessageConversationMessageInternal,
]
