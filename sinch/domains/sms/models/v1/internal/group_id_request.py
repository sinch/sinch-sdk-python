from pydantic import Field, StrictStr

from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class GroupIdRequest(BaseModelConfigurationRequest):
    group_id: StrictStr = Field(
        default=...,
        description="ID of the group.",
    )