from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ServiceIdRequest(BaseModelConfiguration):
    service_id: StrictStr = Field(
        default=...,
        description="The ID of the service.",
        alias="serviceId",
    )
