from typing import Any, Dict, Optional

from pydantic import Field, StrictBool, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.types.conversation_channel_type import (
    ConversationChannelType,
)


class CreateConversationRequest(BaseModelConfiguration):
    app_id: StrictStr = Field(description="The ID of the participating app.")
    contact_id: StrictStr = Field(
        description="The ID of the participating contact."
    )
    active: Optional[StrictBool] = Field(
        default=None,
        description="Flag for whether this conversation is active.",
    )
    active_channel: Optional[ConversationChannelType] = None
    metadata: Optional[StrictStr] = Field(
        default=None,
        description="Arbitrary data set by the Conversation API clients. Up to 1024 characters long. NOTE: This field has been deprecated due to changes in the system architecture or functionality. It is no longer actively maintained and may be removed in future versions. Please avoid relying on this field in new code.",
    )
    metadata_json: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Arbitrary data set by the Conversation API clients and/or provided in the `conversation_metadata` field of a SendMessageRequest. A valid JSON object.",
    )
    correlation_id: Optional[StrictStr] = Field(
        default=None,
        description="Arbitrary correlation ID related to the MT message set by the Conversation API user.",
    )
