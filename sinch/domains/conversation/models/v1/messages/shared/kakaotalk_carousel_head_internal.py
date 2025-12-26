from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class KakaoTalkCarouselHeadInternal(BaseModelConfigurationResponse):
    header: StrictStr = Field(
        ..., description="Carousel introduction title", max_length=20
    )
    content: StrictStr = Field(
        ..., description="Carousel introduction description", max_length=50
    )
    image_url: StrictStr = Field(
        ..., description="URL to the image displayed in the introduction"
    )
    link_mo: Optional[StrictStr] = Field(
        default=None, description="URL opened on a mobile device"
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
