from typing import List, Optional

from pydantic import Field, StrictStr, conlist

from sinch.domains.conversation.models.v1.contacts.response.contact_response import (
    ContactResponse,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ListContactsResponse(BaseModelConfiguration):
    contacts: Optional[conlist(ContactResponse)] = Field(
        default=None,
        description="List of contacts belonging to the specified project.",
    )
    next_page_token: Optional[StrictStr] = Field(
        default=None,
        description="Token that should be included in the next list contacts request to fetch the next page.",
    )

    @property
    def content(self) -> List[ContactResponse]:
        return self.contacts or []
