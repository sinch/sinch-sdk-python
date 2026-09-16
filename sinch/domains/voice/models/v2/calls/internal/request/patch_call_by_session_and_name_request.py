from pydantic import Field, StrictStr, conlist

from sinch.domains.voice.models.v2.request.idempotency_key_request import (
    IdempotencyKeyRequest,
)
from sinch.domains.voice.models.v2.svaml.shared.svaml_command import (
    SvamlCommand,
)


class PatchCallBySessionAndNameRequest(IdempotencyKeyRequest):
    session_id: StrictStr = Field(
        default=...,
        description="The ID of the session.",
        alias="sessionId",
    )
    call_name: StrictStr = Field(
        default=...,
        description="The name of the call leg within the session, as assigned by the `callName` property in the `dial` command.",
        alias="callName",
    )
    commands: conlist(SvamlCommand) = Field(
        default=...,
        description="An ordered list of SVAML v2 (Sinch Voice Application Markup Language) commands that describe a call flow. Commands are executed sequentially in the order they are defined.",
    )
