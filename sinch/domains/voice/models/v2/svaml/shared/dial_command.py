from typing import Literal, Optional

from pydantic import Field, StrictInt, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.shared.call_destination import (
    CallDestination,
)
from sinch.domains.voice.models.v2.svaml.shared.call_events import CallEvents
from sinch.domains.voice.models.v2.shared.call_origin import CallOrigin


class DialCommand(BaseModelConfiguration):
    command: Literal["dial"] = Field(
        default="dial", description="Command to initiate a new call"
    )
    call_name: Optional[StrictStr] = Field(
        default=None,
        alias="callName",
        description="Identifier for this call leg within the session. Must be unique across all active call legs in the session.\n\nOther commands (e.g., `hangup`) can reference this name to target this specific leg.",
    )
    from_: Optional[CallOrigin] = Field(
        default=None,
        alias="from",
    )
    to: CallDestination = Field(
        default=...,
    )
    dial_timeout_duration_seconds: Optional[StrictInt] = Field(
        default=None,
        alias="dialTimeoutDurationSeconds",
        description="Maximum time in seconds to wait for the call to be answered. If the timeout expires without an answer, the `onTimeout` event is triggered.",
    )
    max_call_duration_seconds: Optional[StrictInt] = Field(
        default=None,
        alias="maxCallDurationSeconds",
        description="Maximum duration of the call in seconds. The call is terminated automatically when this limit is reached.",
    )
    events: Optional[CallEvents] = Field(default=None)
