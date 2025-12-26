from typing import Literal, Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_button_internal import (
    KakaoTalkButtonInternal,
)


class KakaoTalkWebLinkButtonInternal(KakaoTalkButtonInternal):
    type: Literal["WL"] = Field("WL", description="Button type")
    link_mo: StrictStr = Field(
        ..., description="URL opened on a mobile device"
    )
    link_pc: Optional[StrictStr] = Field(
        default=None, description="URL opened on a desktop device"
    )
