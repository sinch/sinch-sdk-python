from typing import Optional
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.types.carousel_message_internal import (
    CarouselMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class CarouselMessageFieldInternal(BaseModelConfigurationResponse):
    carousel_message: Optional[CarouselMessageInternal] = None
