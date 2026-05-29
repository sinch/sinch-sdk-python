from sinch.domains.sms.models.v1.internal.group_request import GroupRequest
from sinch.domains.sms.models.v1.shared.group_id_mixin import GroupIdMixin


class ReplaceGroupRequest(GroupIdMixin, GroupRequest):
    """Request model for replacing a group."""

    pass
