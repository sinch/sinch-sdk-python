from typing import Literal
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_button_internal import (
    KakaoTalkButtonInternal,
)


class KakaoTalkAppLinkButtonInternal(KakaoTalkButtonInternal):
    type: Literal["AL"] = Field("AL", description="Button type")
    scheme_ios: StrictStr = Field(
        ...,
        description="App link opened on an iOS device (e.g. `tel://PHONE_NUMBER`)",
    )
    scheme_android: StrictStr = Field(
        ...,
        description="App link opened on an Android device (e.g. `tel://PHONE_NUMBER`)",
    )
