from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class KakaoTalkCarouselTailInternal(BaseModelConfigurationResponse):
    link_mo: StrictStr = Field(
        ..., description="URL opened on a mobile device"
    )
    link_pc: Optional[StrictStr] = Field(
        default=None, description="URL opened on a desktop device"
    )
    scheme_ios: Optional[StrictStr] = Field(
        default=None,
        description="App link opened on an iOS device (e.g. `tel://PHONE_NUMBER`)",
    )
    scheme_android: Optional[StrictStr] = Field(
        default=None,
        description="App link opened on an Android device (e.g. `tel://PHONE_NUMBER`)",
    )
