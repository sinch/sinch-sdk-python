from typing import Optional

from pydantic import Field, StrictStr, conlist

from sinch.domains.voice.models.v2.request.idempotency_key_request import (
    IdempotencyKeyRequest,
)
from sinch.domains.voice.models.v2.svaml.shared.svaml_command import (
    SvamlCommand,
)


class StartCallRequest(IdempotencyKeyRequest):
    commands: conlist(SvamlCommand) = Field(
        default=...,
        description="An ordered list of SVAML v2 (Sinch Voice Application Markup Language) commands that describe a call flow. Commands are executed sequentially in the order they are defined.",
    )
    service_id: Optional[StrictStr] = Field(
        default=None,
        alias="serviceId",
        description="The ID of the service to use for the call. If omitted, the project's default service is used.",
    )
