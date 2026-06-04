from typing import List

from pydantic import StrictStr, conlist

from sinch.domains.sms.models.v1.internal.base import BaseModelConfigurationResponse


class ListGroupMembersResponse(BaseModelConfigurationResponse):
    members: conlist(StrictStr)

    @property
    def content(self) -> List[str]:
        return self.members
