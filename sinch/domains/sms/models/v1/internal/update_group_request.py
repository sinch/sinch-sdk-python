from typing import Optional

from pydantic import Field, StrictStr, conlist

from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)
from sinch.domains.sms.models.v1.shared.auto_update import AutoUpdate
from sinch.domains.sms.models.v1.shared.group_id_mixin import GroupIdMixin


class UpdateGroupRequest(GroupIdMixin, BaseModelConfigurationRequest):
    """Request model for updating a group (incremental changes)."""

    add: Optional[conlist(StrictStr)] = Field(
        default=None,
        description="List of phone numbers (MSISDNs) in E.164 format to add to the group.",
    )
    remove: Optional[conlist(StrictStr)] = Field(
        default=None,
        description="List of phone numbers (MSISDNs) in E.164 format to remove from the group.",
    )
    name: Optional[StrictStr] = Field(
        default=None,
        description=(
            "Name of the group. Omit to leave the name unchanged; "
            "set explicitly to null to remove the existing name."
        ),
    )
    add_from_group: Optional[StrictStr] = Field(
        default=None,
        description="Copy the members from another group into this group. Must be a valid group ID.",
    )
    remove_from_group: Optional[StrictStr] = Field(
        default=None,
        description="Remove the members in a specified group from this group. Must be a valid group ID.",
    )
    auto_update: Optional[AutoUpdate] = Field(
        default=None,
        description="Configuration for auto-subscription via MO keywords.",
    )
