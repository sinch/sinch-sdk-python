from typing import List, Optional

from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.sinch_events.incoming_call_events import (
    IncomingCallResponseEvents,
)
from sinch.domains.voice.models.v2.svaml.shared.svaml_command import (
    SvamlCommand,
)


class VoiceSinchEventResponse(BaseModelConfiguration):
    commands: List[SvamlCommand] = Field(
        default=...,
        description="The ordered list of SVAML commands to execute. Contains at least one command.",
    )
    call_name: Optional[StrictStr] = Field(
        default=None,
        alias="callName",
        description="""Name of the call.

**Note:** This property only takes effect in responses to sinch events triggered by an incoming call. In responses to other sinch event types, it is ignored.""",
    )
    events: Optional[IncomingCallResponseEvents] = Field(
        default=None,
        description="""Commands to execute on specific events for this call.

**Note:** This property only takes effect in responses to sinch events triggered by an incoming call. In responses to other sinch event types, it is ignored.""",
    )
