from typing import Optional
from pydantic import Field, StrictStr, conlist
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.sms.models.v1.shared.mo_media_item import MOMediaItem


class MOMediaBody(BaseModelConfigurationResponse):
    subject: Optional[StrictStr] = Field(
        default=None, description="The subject of the MMS media message."
    )
    message: Optional[StrictStr] = Field(
        default=None,
        description="The text message content of the MMS media message.",
    )
    media: Optional[conlist(MOMediaItem)] = Field(
        default=None,
        description="Collection of attachments in incoming message.",
    )
