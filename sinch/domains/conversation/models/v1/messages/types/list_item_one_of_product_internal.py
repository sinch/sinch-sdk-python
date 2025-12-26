from typing import Optional
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.shared.product_item import (
    ProductItem,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ListItemOneOfProductInternal(BaseModelConfigurationResponse):
    product: ProductItem = Field(...)
