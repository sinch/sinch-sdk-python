from typing import Literal
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_button_internal import (
    KakaoTalkButtonInternal,
)


class KakaoTalkBotKeywordButtonInternal(KakaoTalkButtonInternal):
    type: Literal["BK"] = Field("BK", description="Button type")
