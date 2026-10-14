from typing import Annotated, Union
from sinch.core.models.internal.unions import ResolveUnion

from sinch.domains.conversation.models.v1.messages.categories.list.list_item_choice import (
    ListItemChoice,
)
from sinch.domains.conversation.models.v1.messages.categories.list.list_item_product import (
    ListItemProduct,
)

ListItem = Annotated[
    Union[
        ListItemChoice,
        ListItemProduct,
    ],
    ResolveUnion(),
]
