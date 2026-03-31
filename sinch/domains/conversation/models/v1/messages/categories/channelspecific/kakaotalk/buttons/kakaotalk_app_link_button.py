from typing import Literal
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.buttons import (
    KakaoTalkButton,
)


class KakaoTalkAppLinkButton(KakaoTalkButton):
    type: Literal["AL"] = Field("AL", description="Button type")
    scheme_ios: StrictStr = Field(
        ...,
        description="App link opened on an iOS device (e.g. `tel://PHONE_NUMBER`)",
    )
    scheme_android: StrictStr = Field(
        ...,
        description="App link opened on an Android device (e.g. `tel://PHONE_NUMBER`)",
    )
