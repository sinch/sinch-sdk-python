from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class BasicAuthCredentials(BaseModelConfiguration):
    password: StrictStr = Field(
        default=..., description="Basic auth password."
    )
    username: StrictStr = Field(
        default=..., description="Basic auth username."
    )
