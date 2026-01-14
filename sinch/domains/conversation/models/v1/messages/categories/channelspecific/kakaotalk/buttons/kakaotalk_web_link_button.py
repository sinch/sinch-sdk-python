from typing import Literal, Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.buttons import (
    KakaoTalkButton,
)


class KakaoTalkWebLinkButton(KakaoTalkButton):
    type: Literal["WL"] = Field("WL", description="Button type")
    link_mo: StrictStr = Field(
        ..., description="URL opened on a mobile device"
    )
    link_pc: Optional[StrictStr] = Field(
        default=None, description="URL opened on a desktop device"
    )
