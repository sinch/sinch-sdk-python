from typing import Optional

from pydantic import Field, StrictStr, conlist

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent


class DocumentFieldData(SinchEvent):
    data: Optional[conlist(StrictStr)] = Field(
        default=None,
        description="The data array contains the string(s) assigned to the corresponding document field.",
    )
