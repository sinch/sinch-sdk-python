from datetime import datetime
from typing import Optional

from pydantic import Field, StrictBool, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ServiceShortResponse(BaseModelConfiguration):
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
        default=...,
        description="The name of the service. Between 1 and 64 characters, with the following regex: `^\\S+(\\s+\\S+)*$`",
    )
    description: Optional[StrictStr] = Field(
        default=None, description=" A description of the service. Maximum 255 characters, with the following regex: `^\\S+(\\s+\\S+)*$`."
    )
    is_default: StrictBool = Field(
        default=...,
        alias="isDefault",
        description="Indicates whether this service is set as the default for the project. The default service is used when no specific service is specified in API requests.",
    )
