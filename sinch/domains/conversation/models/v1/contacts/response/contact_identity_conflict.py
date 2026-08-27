from typing import Optional

from pydantic import Field, StrictStr, conlist

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class ContactIdentityConflict(BaseModelConfiguration):
    identity: Optional[StrictStr] = Field(
        default=None,
        description="The identity value (e.g., phone number) that is duplicated across contacts.",
    )
    channels: Optional[conlist(StrictStr)] = Field(
        default=None,
        description="List of channels where this identity is present.",
    )
    contact_ids: Optional[conlist(StrictStr)] = Field(
        default=None,
        description="List of contact IDs that share this identity.",
    )
