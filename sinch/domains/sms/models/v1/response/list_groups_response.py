from typing import Optional

from pydantic import Field, StrictInt, conlist

from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.sms.models.v1.response.group_response import GroupResponse


class ListGroupsResponse(BaseModelConfigurationResponse):
    count: Optional[StrictInt] = Field(
        default=None,
        description="The total number of entries matching the given filters.",
    )
    page: Optional[StrictInt] = Field(
        default=None, description="The requested page."
    )
    page_size: Optional[StrictInt] = Field(
        default=None,
        description="The number of entries returned in this request.",
    )
    groups: Optional[conlist(GroupResponse)] = Field(
        default=None,
        description="The page of groups matching the given filters.",
    )

    @property
    def content(self):
        """Returns the content of the group list."""
        return self.groups or []
