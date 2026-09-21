from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class InstagramCredentials(BaseModelConfiguration):
    token: StrictStr = Field(default=..., description="The static token.")
    business_account_id: Optional[StrictStr] = Field(
        default=None, description="Required if using the Sinch Facebook App."
    )
