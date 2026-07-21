from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class StaticBearerCredentials(BaseModelConfiguration):
    claimed_identity: StrictStr = Field(
        default=..., description="The claimed identity for the channel."
    )
    token: StrictStr = Field(
        default=..., description="The static bearer token for the channel."
    )
