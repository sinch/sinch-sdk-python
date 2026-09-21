from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.credentials.types.channel_integration_status_type import (
    ChannelIntegrationStatusType,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ChannelIntegrationState(BaseModelConfiguration):
    status: ChannelIntegrationStatusType = Field(...)
    description: Optional[StrictStr] = Field(
        default=None, description="Description in case the integration fails"
    )
