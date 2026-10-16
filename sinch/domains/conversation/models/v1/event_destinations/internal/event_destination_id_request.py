from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class EventDestinationIdRequest(BaseModelConfiguration):
    event_destination_id: StrictStr = Field(
        default=..., description="The unique ID of the event destination."
    )
