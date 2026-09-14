from typing import Dict, Optional

from pydantic import Field, StrictStr, conlist

from sinch.domains.voice.models.v2.calls.internal.request.idempotency_key_request import (
    IdempotencyKeyRequest,
)
from sinch.domains.voice.models.v2.calls.shared.batch_options import (
    BatchOptions,
)
from sinch.domains.voice.models.v2.svaml.shared.svaml_command import (
    SvamlCommand,
)


class StartCallRequest(IdempotencyKeyRequest):
    commands: conlist(SvamlCommand) = Field(
        default=...,
        description="An ordered list of SVAML v2 (Sinch Voice Application Markup Language) commands that describe a call flow. Commands are executed sequentially in the order they are defined.",
    )
    parameters: Optional[conlist(Dict[StrictStr, StrictStr])] = Field(
        default=None,
        description="An array of parameter objects that define values for dynamic placeholders in commands. Each object represents a set of parameters for a single queued call.\n\nUse these parameters to inject customer-defined values into your SVAML commands, enabling personalized call flows without modifying the base command structure.",
    )
    batch_options: Optional[BatchOptions] = Field(
        default=None, alias="batchOptions"
    )
    service_id: Optional[StrictStr] = Field(
        default=None,
        alias="serviceId",
        description="The ID of the service to use for the call. If omitted, the project's default service is used.",
    )
