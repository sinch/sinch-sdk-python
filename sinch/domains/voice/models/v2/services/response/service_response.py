from datetime import datetime
from typing import Optional

from pydantic import Field, StrictBool, StrictStr, model_validator

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.internal.utils.helpers import (
    rename_wire_call_behavior_type,
)
from sinch.domains.voice.models.v2.services.shared.call_behavior import (
    CallBehavior,
)


class ServiceResponse(BaseModelConfiguration):
    service_id: StrictStr = Field(
        default=..., alias="serviceId", description="The ID of the service."
    )
    project_id: StrictStr = Field(
        default=..., alias="projectId", description="The ID of the project."
    )
    create_time: datetime = Field(
        default=...,
        alias="createTime",
        description="Timestamp (RFC 3339) indicating when the service was created.",
    )
    update_time: Optional[datetime] = Field(
        default=None,
        alias="updateTime",
        description="Timestamp (RFC 3339) indicating when the service was last updated.\n\nOmitted if the service has never been updated.",
    )
    name: StrictStr = Field(
        default=..., description="The name of the service. Between 1 and 64 characters, with the following regex: `^\\S+(\\s+\\S+)*$`"
    )
    description: Optional[StrictStr] = Field(
        default=None, description="A description of the service. Maximum 255 characters, with the following regex: `^\\S+(\\s+\\S+)*$`."
    )
    is_default: StrictBool = Field(
        default=...,
        alias="isDefault",
        description="Whether this service is the project default.",
    )
    call_behavior: Optional[CallBehavior] = Field(
        default=None, alias="callBehavior"
    )

    @model_validator(mode="before")
    @classmethod
    def _rename_wire_call_behavior_type(cls, data):
        for field in ("call_behavior", "callBehavior"):
            data = rename_wire_call_behavior_type(data, field=field)
        return data
