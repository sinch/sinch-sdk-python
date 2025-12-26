from typing import Optional
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.conversation.models.v1.messages.types.contact_info_message_internal import (
    ContactInfoMessageInternal,
)


class ContactInfoMessageFieldInternal(BaseModelConfigurationResponse):
    contact_info_message: Optional[ContactInfoMessageInternal] = None
