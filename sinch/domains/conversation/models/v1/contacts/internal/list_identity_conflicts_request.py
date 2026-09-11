from typing import Optional

from pydantic import Field, StrictInt, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ListIdentityConflictsRequest(BaseModelConfiguration):
    page_size: Optional[StrictInt] = Field(
        default=None,
        description="Maximum number of conflicts to return (max 20).",
    )
    page_token: Optional[StrictStr] = Field(
        default=None,
        description="Pagination token for retrieving next page.",
    )
