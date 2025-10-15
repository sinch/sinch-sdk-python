from sinch.domains.numbers.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)
from typing import Optional
from pydantic import Field, StrictStr


class NotFoundErrorDetails(BaseModelConfigurationResponse):
    type: Optional[StrictStr] = Field(default=None, alias="type")
    resource_type: Optional[StrictStr] = Field(
        default=None, alias="resourceType"
    )
    resource_name: Optional[StrictStr] = Field(
        default=None, alias="resourceName"
    )
    owner: Optional[StrictStr] = Field(default=None, alias="owner")
    description: Optional[StrictStr] = Field(default=None, alias="description")
