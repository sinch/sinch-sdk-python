from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class EventIdRequest(BaseModelConfiguration):
    event_id: StrictStr = Field(
        default=..., description="The unique ID of the event."
    )
