from typing import Optional
from pydantic import StrictStr, Field
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationResponse


class CallbackConfigurationResponse(BaseModelConfigurationResponse):
    project_id: Optional[StrictStr] = Field(default=None, alias="projectId")
    hmac_secret: Optional[StrictStr] = Field(default=None, alias="hmacSecret")
