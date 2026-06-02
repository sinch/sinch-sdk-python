

from pydantic import Field

from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class InboundIdRequest(BaseModelConfigurationRequest):
    inbound_id: str = Field(
        default=...,
        description="The unique identifier of the inbound message.",
    )