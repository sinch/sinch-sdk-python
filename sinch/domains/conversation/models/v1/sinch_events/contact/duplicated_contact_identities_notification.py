from typing import Optional

from pydantic import Field, conlist

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent
from sinch.domains.conversation.models.v1.sinch_events.contact.duplicated_identities import (
    DuplicatedIdentities,
)


class DuplicatedContactIdentitiesNotification(SinchEvent):
    duplicated_identities: Optional[conlist(DuplicatedIdentities)] = Field(
        default=None,
        description="Channel identities duplicated between multiple contacts.",
    )
