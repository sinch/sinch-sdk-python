from typing import Optional
from sinch.domains.conversation.models.v1.messages.response.shared.carousel_message import (
    CarouselMessage,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class CarouselMessageField(BaseModelConfigurationResponse):
    carousel_message: Optional[CarouselMessage] = None
