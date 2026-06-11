from datetime import datetime
from typing import Optional

from pydantic import Field, StrictInt, StrictStr, conlist

from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.sms.models.v1.shared.auto_update import AutoUpdate


class GroupResponse(BaseModelConfigurationResponse):
    id: Optional[StrictStr] = Field(
        default=None,
        description="The ID used to reference this group.",
    )
    name: Optional[StrictStr] = Field(
        default=None,
        description="Name of group",
    )
    size: Optional[StrictInt] = Field(
        default=None,
        description="The number of members currently in the group.",
    )
    created_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp for group creation. Format: YYYY-MM-DDThh:mm:ss.SSSZ",
    )
    modified_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp for when the group was last updated. Format: YYYY-MM-DDThh:mm:ss.SSSZ",
    )
    child_groups: Optional[conlist(StrictStr)] = Field(
        default=None,
        description="MSISDNs of child groups will be included in this group. Elements must be group IDs.",
    )
    auto_update: Optional[AutoUpdate] = Field(
        default=None,
        description="Configuration for auto-subscription via MO keywords.",
    )
