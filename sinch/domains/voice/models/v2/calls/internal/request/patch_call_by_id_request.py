from pydantic import Field, StrictStr, conlist

from sinch.domains.voice.models.v2.request.idempotency_key_request import (
    IdempotencyKeyRequest,
)
from sinch.domains.voice.models.v2.svaml.shared.svaml_command import (
    SvamlCommand,
)


class PatchCallByIdRequest(IdempotencyKeyRequest):
    call_id: StrictStr = Field(
        default=...,
        description="The ID of the call.",
        alias="callId",
    )
    commands: conlist(SvamlCommand) = Field(
        default=...,
        description="An ordered list of SVAML v2 (Sinch Voice Application Markup Language) commands that describe a call flow. Commands are executed sequentially in the order they are defined.",
    )
