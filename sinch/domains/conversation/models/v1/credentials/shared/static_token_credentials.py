from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class StaticTokenCredentials(BaseModelConfiguration):
    token: StrictStr = Field(
        default=..., description="The static token for the channel."
    )
