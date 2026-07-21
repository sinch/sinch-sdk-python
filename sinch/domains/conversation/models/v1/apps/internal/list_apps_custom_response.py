from typing import List, Optional

from pydantic import Field, conlist

from sinch.domains.conversation.models.v1.apps.internal.list_apps_response import (
    ListAppsResponse,
)
from sinch.domains.conversation.models.v1.apps.response.app_custom_response import (
    AppCustomResponse,
)


class ListAppsCustomResponse(ListAppsResponse):
    apps: Optional[conlist(AppCustomResponse)] = Field(
        default=None,
        description="List of apps belonging to a specific project ID.",
    )

    @property
    def content(self) -> List[AppCustomResponse]:
        return self.apps or []
