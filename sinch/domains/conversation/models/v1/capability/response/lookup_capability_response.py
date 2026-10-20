from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.messages.internal.request.recipient import (
    Recipient,
)


class LookupCapabilityResponse(BaseModelConfiguration):
    app_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the app to use for capability lookup.",
    )
    recipient: Optional[Recipient] = Field(
        default=None, description="Identifies the recipient."
    )
    request_id: Optional[StrictStr] = Field(
        default=None,
        description="ID for the asynchronous response, will be generated if not set.",
    )
