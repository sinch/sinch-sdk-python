from typing import Optional

from pydantic import Field

from sinch.domains.conversation.models.v1.contacts.response.contact_response import (
    ContactResponse,
)
from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent


class ContactMergeNotification(SinchEvent):
    preserved_contact: Optional[ContactResponse] = Field(
        default=None, description="The contact that was kept after the merge."
    )
    deleted_contact: Optional[ContactResponse] = Field(
        default=None, description="The contact that was removed by the merge."
    )
