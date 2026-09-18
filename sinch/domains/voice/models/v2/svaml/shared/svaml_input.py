from typing import Optional

from pydantic import Field, StrictStr, conlist

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.svaml.shared.incoming_call_response_events import (
    IncomingCallResponseEvents,
)
from sinch.domains.voice.models.v2.svaml.shared.svaml_command import (
    SvamlCommand,
)


class SvamlInput(BaseModelConfiguration):
    commands: conlist(SvamlCommand) = Field(
        default=...,
        description="An ordered list of SVAML v2 (Sinch Voice Application Markup Language) commands that describe a call flow. Commands are executed sequentially in the order they are defined.",
    )
    call_name: Optional[StrictStr] = Field(
        default=None,
        alias="callName",
        description="Name of the call. Must be 1-32 characters. Regex pattern: `^\S+$`",
    )
    events: Optional[IncomingCallResponseEvents] = Field(
        default=None,
        description="Commands to execute on specific events for this call.",
    )
