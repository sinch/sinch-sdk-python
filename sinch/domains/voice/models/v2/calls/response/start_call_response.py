from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class StartCallResponse(BaseModelConfiguration):
    project_id: StrictStr = Field(
        alias="projectId",
        description="The `Id` of the project associated with the call.",
    )
    service_id: StrictStr = Field(
        alias="serviceId",
        description="The ID of the service used.",
    )
    session_id: Optional[StrictStr] = Field(
        default=None,
        alias="sessionId",
        description="The ID of the session.",
    )
    batch_id: Optional[StrictStr] = Field(
        default=None,
        alias="batchId",
        description="The ID of the batch.",
    )
