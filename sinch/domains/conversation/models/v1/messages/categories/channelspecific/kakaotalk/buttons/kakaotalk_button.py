from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class KakaoTalkButton(BaseModelConfiguration):
    name: StrictStr = Field(..., description="Text displayed on the button")
