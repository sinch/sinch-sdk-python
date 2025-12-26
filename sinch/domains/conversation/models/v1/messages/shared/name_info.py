from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class NameInfo(BaseModelConfigurationResponse):
    full_name: StrictStr = Field(
        default=..., description="Full name of the contact"
    )
    first_name: Optional[StrictStr] = Field(
        default=None, description="First name."
    )
    last_name: Optional[StrictStr] = Field(
        default=None, description="Last name."
    )
    middle_name: Optional[StrictStr] = Field(
        default=None, description="Middle name."
    )
    prefix: Optional[StrictStr] = Field(
        default=None,
        description="Prefix before the name. e.g. Mr, Mrs, Dr etc.",
    )
    suffix: Optional[StrictStr] = Field(
        default=None, description="Suffix after the name."
    )
