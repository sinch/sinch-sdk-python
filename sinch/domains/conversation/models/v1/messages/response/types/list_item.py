from typing import Union
from sinch.domains.conversation.models.v1.messages.response.shared.list_item_choice import (
    ListItemChoice,
)
from sinch.domains.conversation.models.v1.messages.response.shared.list_item_product import (
    ListItemProduct,
)


ListItem = Union[ListItemChoice, ListItemProduct]
