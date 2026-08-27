from typing import List, Optional

from pydantic import Field, StrictStr, conlist

from sinch.domains.conversation.models.v1.contacts.response.contact_identity_conflict import (
    ContactIdentityConflict,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ListIdentityConflictsResponse(BaseModelConfiguration):
    conflicts: Optional[conlist(ContactIdentityConflict)] = Field(
        default=None,
        description="List of contact identity conflicts.",
    )
    next_page_token: Optional[StrictStr] = Field(
        default=None,
        description="Token for retrieving the next page of results.",
    )

    @property
    def content(self) -> List[ContactIdentityConflict]:
        return self.conflicts or []
