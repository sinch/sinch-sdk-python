from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.messages.internal.request.recipient import (
    Recipient,
)


class LookupCapabilityRequest(BaseModelConfiguration):
    app_id: StrictStr = Field(
        description="The ID of the app to use for capability lookup."
    )
    recipient: Recipient = Field(description="Identifies the recipient.")
    request_id: Optional[StrictStr] = Field(
        default=None,
        description="ID for the asynchronous response, will be generated if not set. Currently this field is not used for idempotency.",
    )
