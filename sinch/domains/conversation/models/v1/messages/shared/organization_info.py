from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class OrganizationInfo(BaseModelConfigurationResponse):
    company: Optional[StrictStr] = Field(
        default=None, description="Company name"
    )
    department: Optional[StrictStr] = Field(
        default=None, description="Department at the company"
    )
    title: Optional[StrictStr] = Field(
        default=None, description="Corporate title, e.g. Software engineer"
    )
