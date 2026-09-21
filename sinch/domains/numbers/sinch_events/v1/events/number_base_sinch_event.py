from datetime import datetime
from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.numbers.sinch_events.v1.events.resource_type import (
    ResourceType,
)
from sinch.domains.numbers.sinch_events.v1.internal.sinch_event import (
    SinchEvent,
)


class NumberBaseSinchEvent(SinchEvent):
    event_id: Optional[StrictStr] = Field(
        default=None, alias="eventId", description="The ID of the event."
    )
    timestamp: Optional[datetime] = Field(
        default=None,
        description="The date and time when the callback was created and added to the callbacks queue.",
    )
    project_id: Optional[StrictStr] = Field(
        default=None,
        alias="projectId",
        description="The ID of the project to which the event belongs.",
    )
    resource_type: ResourceType = Field(default=..., alias="resourceType")
