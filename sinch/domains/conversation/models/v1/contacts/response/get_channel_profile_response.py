from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class GetChannelProfileResponse(BaseModelConfiguration):
    profile_name: Optional[StrictStr] = Field(
        default=None, description="The profile name."
    )
