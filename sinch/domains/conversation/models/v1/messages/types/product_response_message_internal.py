from typing import Optional
from pydantic import Field, StrictStr, conlist
from sinch.domains.conversation.models.v1.messages.shared.product_item import (
    ProductItem,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ProductResponseMessageInternal(BaseModelConfigurationResponse):
    products: Optional[conlist(ProductItem)] = Field(
        default=None, description="The selected products."
    )
    title: Optional[StrictStr] = Field(
        default=None,
        description="Optional parameter. Text that may be sent with selected products.",
    )
    catalog_id: Optional[StrictStr] = Field(
        default=None,
        description="Optional parameter. The catalog id that the selected products belong to.",
    )
