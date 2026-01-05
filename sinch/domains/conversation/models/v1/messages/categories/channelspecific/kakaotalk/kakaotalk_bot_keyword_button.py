from typing import Literal
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.kakaotalk_button import (
    KakaoTalkButton,
)


class KakaoTalkBotKeywordButton(KakaoTalkButton):
    type: Literal["BK"] = Field("BK", description="Button type")
