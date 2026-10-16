from typing import List, Optional

from pydantic import Field, conlist

from sinch.domains.conversation.models.v1.event_destinations.response.event_destination_response import (
    EventDestinationResponse,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ListEventDestinationsResponse(BaseModelConfiguration):
    event_destinations: Optional[conlist(EventDestinationResponse)] = Field(
        default=None,
        alias="webhooks",
        description="List of event destinations belonging to a specific project ID and app ID",
    )

    @property
    def content(self) -> List[EventDestinationResponse]:
        return self.event_destinations or []
