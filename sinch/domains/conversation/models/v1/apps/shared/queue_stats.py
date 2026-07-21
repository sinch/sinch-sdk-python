from typing import Optional
from pydantic import Field, StrictInt
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class QueueStats(BaseModelConfiguration):
    outbound_size: Optional[StrictInt] = Field(
        default=None, description="The current size of the App's MT queue."
    )
    outbound_limit: Optional[StrictInt] = Field(
        default=None,
        description="The limit of the App's MT queue. The default limit is 500000 messages.",
    )
