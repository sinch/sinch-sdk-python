from typing import Optional
from sinch.domains.conversation.models.v1.messages.categories.carousel.carousel_message import (
    CarouselMessage,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class CarouselMessageField(BaseModelConfiguration):
    carousel_message: Optional[CarouselMessage] = None
