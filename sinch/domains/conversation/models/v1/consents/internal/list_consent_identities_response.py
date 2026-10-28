from typing import List, Optional

from pydantic import Field, StrictStr, conlist

from sinch.domains.conversation.models.v1.consents.response.consent_identity_response import (
    ConsentIdentityResponse,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ListConsentIdentitiesResponse(BaseModelConfiguration):
    identities: Optional[conlist(ConsentIdentityResponse)] = Field(
        default=None,
        description="List of identities belonging to a specific project ID, app ID, and list type",
    )
    next_page_token: Optional[StrictStr] = Field(
        default=None,
        description="Token for the next page of the search, to be used in the next call.",
    )

    @property
    def content(self) -> List[ConsentIdentityResponse]:
        return self.identities or []
