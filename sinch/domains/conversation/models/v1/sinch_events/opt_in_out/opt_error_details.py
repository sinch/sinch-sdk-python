from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent


class OptErrorDetails(SinchEvent):
    description: Optional[StrictStr] = Field(
        default=None, description="Human-readable error description."
    )
