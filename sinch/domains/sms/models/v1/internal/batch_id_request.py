from pydantic import Field, StrictStr
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class BatchIdRequest(BaseModelConfigurationRequest):
    batch_id: StrictStr = Field(
        default=...,
        description="The unique identifier of the batch message.",
    )
