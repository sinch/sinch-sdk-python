from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ListMessagePropertiesInternal(BaseModelConfigurationResponse):
    catalog_id: Optional[StrictStr] = Field(
        default=None,
        description="Required if sending a product list message. The ID of the catalog to which the products belong.",
    )
    menu: Optional[StrictStr] = Field(
        default=None,
        description="Optional. Sets the text for the menu of a choice list message.",
    )
    whatsapp_header: Optional[StrictStr] = Field(
        default=None,
        description="Optional. Sets the text for the header of a WhatsApp choice list message. Ignored for other channels.",
    )
