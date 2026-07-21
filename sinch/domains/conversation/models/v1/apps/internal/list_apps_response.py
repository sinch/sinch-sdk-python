from typing import List, Optional
from pydantic import Field, conlist
from sinch.domains.conversation.models.v1.apps.response.app_response import (
    AppResponse,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ListAppsResponse(BaseModelConfiguration):
    apps: Optional[conlist(AppResponse)] = Field(
        default=None,
        description="List of apps belonging to a specific project ID.",
    )

    @property
    def content(self) -> List[AppResponse]:
        return self.apps or []
