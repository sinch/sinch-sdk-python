from typing import Literal
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class KakaoTalkButtonInternal(BaseModelConfigurationResponse):
    name: StrictStr = Field(..., description="Text displayed on the button")
