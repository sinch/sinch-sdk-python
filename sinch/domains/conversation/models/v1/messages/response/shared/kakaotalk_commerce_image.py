from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class KakaoTalkCommerceImage(BaseModelConfigurationResponse):
    image_url: StrictStr = Field(..., description="URL to the product image")
    image_link: Optional[StrictStr] = Field(
        default=None, description="URL opened when a user clicks on the image"
    )
