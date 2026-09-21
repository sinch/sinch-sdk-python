from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class TelegramCredentials(BaseModelConfiguration):
    token: StrictStr = Field(
        default=...,
        description="The token for the Telegram bot to which you are connecting.",
    )
