from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class EventDestinationSettings(BaseModelConfiguration):
    secret_for_overridden_target: Optional[StrictStr] = Field(
        default=None,
        alias="secret_for_overridden_callback_urls",
        description="Optional. Secret can be used to sign contents of delivery receipts for a message that was sent with the default event destination target overridden (using the [`event_destination_target` field](https://developers.sinch.com/docs/conversation/api-reference/conversation/tag/Messages/#tag/Messages/operation/Messages_SendMessage!path=callback_url&t=request)). You can then use the secret to verify the signature.",
    )
