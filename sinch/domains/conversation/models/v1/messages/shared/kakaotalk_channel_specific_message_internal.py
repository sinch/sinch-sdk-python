from typing import Optional
from pydantic import Field, StrictBool
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class KakaoTalkChannelSpecificMessageInternal(BaseModelConfigurationResponse):
    push_alarm: Optional[StrictBool] = Field(
        default=True,
        description="Set to `true` if a push alarm should be sent to a device.",
    )
    adult: Optional[StrictBool] = Field(
        default=False,
        description="Set to `true` if a message contains adult content. Set to `false` by default.",
    )
