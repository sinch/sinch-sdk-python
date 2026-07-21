from typing import Optional

from pydantic import Field, StrictBool, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class LineCredentials(BaseModelConfiguration):
    token: StrictStr = Field(
        default=...,
        description="The token for the LINE channel to which you are connecting.",
    )
    secret: StrictStr = Field(
        default=...,
        description="The secret for the LINE channel to which you are connecting.",
    )
    is_default: Optional[StrictBool] = Field(
        default=None,
        description="When an app contains multiple LINE or LINE Enterprise credentials, one of the credentials needs to be defined as the default. Setting this property to `true` marks the corresponding credentials as the default credentials.",
    )
