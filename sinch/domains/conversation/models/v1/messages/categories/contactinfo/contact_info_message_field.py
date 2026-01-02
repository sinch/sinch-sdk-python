from typing import Optional
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.conversation.models.v1.messages.categories.contactinfo.contact_info_message import (
    ContactInfoMessage,
)


class ContactInfoMessageField(BaseModelConfigurationResponse):
    contact_info_message: Optional[ContactInfoMessage] = None
