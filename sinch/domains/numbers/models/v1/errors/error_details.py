from sinch.domains.numbers.models.v1.internal import BaseModelConfigResponse
from typing import Optional
from pydantic import Field, StrictStr


class ErrorDetails(BaseModelConfigResponse):
    type: Optional[StrictStr] = Field(default=None, alias="type")
    resource_type: Optional[StrictStr] = Field(default=None, alias="resourceType")
    resource_name: Optional[StrictStr] = Field(default=None, alias="resourceName")
    owner: Optional[StrictStr] = Field(default=None, alias="owner")
    description: Optional[StrictStr] = Field(default=None, alias="description")
