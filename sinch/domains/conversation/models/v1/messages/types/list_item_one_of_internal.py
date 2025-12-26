from typing import Union
from sinch.domains.conversation.models.v1.messages.types.list_item_one_of_choice_internal import (
    ListItemOneOfChoiceInternal,
)
from sinch.domains.conversation.models.v1.messages.types.list_item_one_of_product_internal import (
    ListItemOneOfProductInternal,
)


ListItemOneOfInternal = Union[
    ListItemOneOfChoiceInternal, ListItemOneOfProductInternal
]
