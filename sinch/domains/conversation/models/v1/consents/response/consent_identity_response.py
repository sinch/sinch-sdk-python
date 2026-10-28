from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ConsentIdentityResponse(BaseModelConfiguration):
    identity: StrictStr = Field(
        default=..., description="The identity from Conversation API."
    )
