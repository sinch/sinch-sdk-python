from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class StartBatchResponse(BaseModelConfiguration):
    project_id: StrictStr = Field(
        alias="projectId",
        description="The `Id` of the project associated with the call.",
    )
    service_id: StrictStr = Field(
        alias="serviceId",
        description="The ID of the service used.",
    )
    batch_id: StrictStr = Field(
        alias="batchId",
        description="The ID of the batch.",
    )
