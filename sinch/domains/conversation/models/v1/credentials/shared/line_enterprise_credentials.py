from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class LineEnterpriseCredentials(BaseModelConfiguration):
    token: StrictStr = Field(
        default=...,
        description="The token for the LINE channel to which you are connecting.",
    )
    secret: StrictStr = Field(
        default=...,
        description="The secret for the LINE channel to which you are connecting.",
    )
