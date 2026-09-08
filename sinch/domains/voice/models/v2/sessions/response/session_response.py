from datetime import datetime
from typing import Optional

from pydantic import Field, StrictStr, conlist

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.shared.call import Call
from sinch.domains.voice.models.v2.types.session_state import SessionState


class SessionResponse(BaseModelConfiguration):
    session_id: StrictStr = Field(
        default=..., alias="sessionId", description="The ID of the session."
    )
    project_id: StrictStr = Field(
        default=...,
        alias="projectId",
        description="The `Id` of the project associated with the call.",
    )
    service_id: StrictStr = Field(
        default=...,
        alias="serviceId",
        description="The ID of the service used.",
    )
    calls: conlist(Call) = Field(default=...)
    create_time: datetime = Field(
        default=...,
        alias="createTime",
        description="Timestamp (RFC 3339) indicating when the session was created.",
    )
    update_time: Optional[datetime] = Field(
        default=None,
        alias="updateTime",
        description="Timestamp (RFC 3339) indicating when the session was last updated.\n\nOmitted if no updates were performed on this session.",
    )
    end_time: Optional[datetime] = Field(
        default=None,
        alias="endTime",
        description="Timestamp (RFC 3339) indicating when the session ended.\n\nOmitted for ongoing sessions.",
    )
    state: SessionState = Field(default=...)
