from typing import Optional
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.messages.categories.contactinfo.contact_info_message import (
    ContactInfoMessage,
)


class ContactInfoMessageField(BaseModelConfiguration):
    contact_info_message: Optional[ContactInfoMessage] = None
