from typing import Optional

from pydantic import Field, StrictStr, conlist

from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)
from sinch.domains.sms.models.v1.shared.auto_update import AutoUpdate


class GroupRequest(BaseModelConfigurationRequest):
    name: Optional[StrictStr] = Field(
        default=None,
        description="Name of group",
    )
    members: Optional[conlist(StrictStr)] = Field(
        default=None,
        description="Initial list of phone numbers in [E.164 format] for the group.",
    )
    child_groups: Optional[conlist(StrictStr)] = Field(
        default=None,
        description="MSISDNs of child groups will be included in this group. Elements must be group IDs.",
    )
    auto_update: Optional[AutoUpdate] = Field(
        default=None,
        description="Configuration for auto-subscription via MO keywords.",
    )
