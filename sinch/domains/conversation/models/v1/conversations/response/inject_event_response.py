from datetime import datetime
from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class InjectEventResponse(BaseModelConfiguration):
    event_id: Optional[StrictStr] = Field(
        default=None, description="Event id."
    )
    accepted_time: Optional[datetime] = None
