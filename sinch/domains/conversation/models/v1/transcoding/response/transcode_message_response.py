from typing import Dict, Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class TranscodeMessageResponse(BaseModelConfiguration):
    transcoded_message: Optional[Dict[str, StrictStr]] = Field(
        default=None,
        description="The transcoded message for the different channels. The keys in the map correspond to channel names, as defined by the type ConversationChannel.",
    )
