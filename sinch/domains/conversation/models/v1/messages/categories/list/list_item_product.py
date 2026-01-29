from pydantic import Field
from sinch.domains.conversation.models.v1.messages.shared.product_item import (
    ProductItem,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class ListItemProduct(BaseModelConfiguration):
    product: ProductItem = Field(...)
