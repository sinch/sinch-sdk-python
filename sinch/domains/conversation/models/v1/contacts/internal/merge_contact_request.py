from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.contacts.types.conversation_merge_strategy_type import (
    ConversationMergeStrategyType,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class MergeContactRequest(BaseModelConfiguration):
    destination_id: StrictStr = Field(
        description="The unique ID of the contact that should be kept when merging two contacts."
    )
    source_id: StrictStr = Field(
        description="Required. The ID of the contact that should be removed."
    )
    strategy: Optional[ConversationMergeStrategyType] = Field(
        default=None,
        description="The merge strategy to apply. The server default is `MERGE`.",
    )
